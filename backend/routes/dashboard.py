from flask import Blueprint, jsonify, g
from models import Task, ProjectMember
from middleware import token_required
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard():
    # Get all projects user is a member of
    memberships = ProjectMember.query.filter_by(user_id=g.current_user.id).all()
    project_ids = [m.project_id for m in memberships]

    # Get all tasks across user's projects
    all_tasks = Task.query.filter(Task.project_id.in_(project_ids)).all()

    # Tasks assigned to current user
    my_tasks = [t for t in all_tasks if t.assigned_to == g.current_user.id]

    now = datetime.utcnow()
    overdue_tasks = [
        t for t in all_tasks
        if t.due_date and t.due_date < now and t.status != 'done'
    ]

    stats = {
        'total_projects': len(project_ids),
        'total_tasks': len(all_tasks),
        'my_tasks': len(my_tasks),
        'todo': len([t for t in all_tasks if t.status == 'todo']),
        'in_progress': len([t for t in all_tasks if t.status == 'in_progress']),
        'done': len([t for t in all_tasks if t.status == 'done']),
        'overdue': len(overdue_tasks),
    }

    recent_tasks = sorted(all_tasks, key=lambda t: t.updated_at or t.created_at, reverse=True)[:10]

    return jsonify({
        'stats': stats,
        'recent_tasks': [t.to_dict() for t in recent_tasks],
        'overdue_tasks': [t.to_dict() for t in overdue_tasks]
    })
