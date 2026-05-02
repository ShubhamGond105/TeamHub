from flask import Blueprint, request, jsonify, g
from models import db, Task, ProjectMember
from middleware import token_required
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
@token_required
def list_tasks(project_id):
    membership = ProjectMember.query.filter_by(
        project_id=project_id, user_id=g.current_user.id
    ).first()
    if not membership:
        return jsonify({'error': 'Access denied'}), 403

    query = Task.query.filter_by(project_id=project_id)

    status = request.args.get('status')
    if status:
        query = query.filter_by(status=status)

    priority = request.args.get('priority')
    if priority:
        query = query.filter_by(priority=priority)

    assigned_to = request.args.get('assigned_to')
    if assigned_to:
        query = query.filter_by(assigned_to=int(assigned_to))

    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify({'tasks': [t.to_dict() for t in tasks]})


@tasks_bp.route('/projects/<int:project_id>/tasks', methods=['POST'])
@token_required
def create_task(project_id):
    membership = ProjectMember.query.filter_by(
        project_id=project_id, user_id=g.current_user.id
    ).first()
    if not membership or membership.role != 'admin':
        return jsonify({'error': 'Only admins can create tasks'}), 403

    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Task title is required'}), 400

    due_date = None
    if data.get('due_date'):
        try:
            due_date = datetime.fromisoformat(data['due_date'])
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

    # Validate assigned_to is a project member
    if data.get('assigned_to'):
        member_check = ProjectMember.query.filter_by(
            project_id=project_id, user_id=data['assigned_to']
        ).first()
        if not member_check:
            return jsonify({'error': 'Assigned user is not a project member'}), 400

    task = Task(
        title=data['title'].strip(),
        description=data.get('description', '').strip(),
        status=data.get('status', 'todo'),
        priority=data.get('priority', 'medium'),
        due_date=due_date,
        project_id=project_id,
        assigned_to=data.get('assigned_to'),
        created_by=g.current_user.id
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({'task': task.to_dict(), 'message': 'Task created'}), 201


@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
@token_required
def get_task(task_id):
    task = Task.query.get_or_404(task_id)

    membership = ProjectMember.query.filter_by(
        project_id=task.project_id, user_id=g.current_user.id
    ).first()
    if not membership:
        return jsonify({'error': 'Access denied'}), 403

    return jsonify({'task': task.to_dict()})


@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)

    membership = ProjectMember.query.filter_by(
        project_id=task.project_id, user_id=g.current_user.id
    ).first()
    if not membership:
        return jsonify({'error': 'Access denied'}), 403

    data = request.get_json()

    # Members can only update status of their assigned tasks
    if membership.role == 'member':
        if task.assigned_to != g.current_user.id:
            return jsonify({'error': 'You can only update tasks assigned to you'}), 403
        if set(data.keys()) - {'status'}:
            return jsonify({'error': 'Members can only update task status'}), 403
        if data.get('status') not in ['todo', 'in_progress', 'done']:
            return jsonify({'error': 'Invalid status'}), 400
        task.status = data['status']
    else:
        # Admin can update everything
        if data.get('title'):
            task.title = data['title'].strip()
        if 'description' in data:
            task.description = data['description'].strip()
        if data.get('status'):
            task.status = data['status']
        if data.get('priority'):
            task.priority = data['priority']
        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.fromisoformat(data['due_date'])
                except ValueError:
                    return jsonify({'error': 'Invalid date format'}), 400
            else:
                task.due_date = None
        if 'assigned_to' in data:
            if data['assigned_to']:
                member_check = ProjectMember.query.filter_by(
                    project_id=task.project_id, user_id=data['assigned_to']
                ).first()
                if not member_check:
                    return jsonify({'error': 'Assigned user is not a project member'}), 400
            task.assigned_to = data['assigned_to']

    task.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({'task': task.to_dict(), 'message': 'Task updated'})


@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    membership = ProjectMember.query.filter_by(
        project_id=task.project_id, user_id=g.current_user.id
    ).first()
    if not membership or membership.role != 'admin':
        return jsonify({'error': 'Only admins can delete tasks'}), 403

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'})
