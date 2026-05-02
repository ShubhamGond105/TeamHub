from flask import Blueprint, request, jsonify, g
from models import db, Project, ProjectMember
from middleware import token_required

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('', methods=['GET'])
@token_required
def list_projects():
    memberships = ProjectMember.query.filter_by(user_id=g.current_user.id).all()
    project_ids = [m.project_id for m in memberships]
    projects = Project.query.filter(Project.id.in_(project_ids)).order_by(Project.created_at.desc()).all()

    result = []
    for project in projects:
        p = project.to_dict()
        membership = next((m for m in memberships if m.project_id == project.id), None)
        p['user_role'] = membership.role if membership else None
        p['creator'] = project.creator.to_dict() if project.creator else None
        result.append(p)

    return jsonify({'projects': result})


@projects_bp.route('', methods=['POST'])
@token_required
def create_project():
    if getattr(g.current_user, 'role', 'member') != 'admin':
        return jsonify({'error': 'Only system admins can create new projects'}), 403

    data = request.get_json()

    if not data or not data.get('name'):
        return jsonify({'error': 'Project name is required'}), 400

    project = Project(
        name=data['name'].strip(),
        description=data.get('description', '').strip(),
        created_by=g.current_user.id
    )
    db.session.add(project)
    db.session.flush()

    # Add creator as admin member
    member = ProjectMember(
        project_id=project.id,
        user_id=g.current_user.id,
        role='admin'
    )
    db.session.add(member)
    db.session.commit()

    return jsonify({'project': project.to_dict(), 'message': 'Project created successfully'}), 201


@projects_bp.route('/<int:project_id>', methods=['GET'])
@token_required
def get_project(project_id):
    project = Project.query.get_or_404(project_id)

    membership = ProjectMember.query.filter_by(
        project_id=project_id, user_id=g.current_user.id
    ).first()
    if not membership:
        return jsonify({'error': 'Access denied'}), 403

    p = project.to_dict()
    p['user_role'] = membership.role
    p['creator'] = project.creator.to_dict() if project.creator else None

    return jsonify({'project': p})


@projects_bp.route('/<int:project_id>', methods=['PUT'])
@token_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)

    membership = ProjectMember.query.filter_by(
        project_id=project_id, user_id=g.current_user.id
    ).first()
    if not membership or membership.role != 'admin':
        return jsonify({'error': 'Only admins can update the project'}), 403

    data = request.get_json()
    if data.get('name'):
        project.name = data['name'].strip()
    if 'description' in data:
        project.description = data['description'].strip()

    db.session.commit()
    return jsonify({'project': project.to_dict(), 'message': 'Project updated'})


@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@token_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    membership = ProjectMember.query.filter_by(
        project_id=project_id, user_id=g.current_user.id
    ).first()
    if not membership or membership.role != 'admin':
        return jsonify({'error': 'Only admins can delete the project'}), 403

    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'})
