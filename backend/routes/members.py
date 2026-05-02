from flask import Blueprint, request, jsonify, g
from models import db, User, ProjectMember
from middleware import token_required

members_bp = Blueprint('members', __name__)


@members_bp.route('/projects/<int:project_id>/members', methods=['GET'])
@token_required
def list_members(project_id):
    membership = ProjectMember.query.filter_by(
        project_id=project_id, user_id=g.current_user.id
    ).first()
    if not membership:
        return jsonify({'error': 'Access denied'}), 403

    members = ProjectMember.query.filter_by(project_id=project_id).all()
    return jsonify({'members': [m.to_dict() for m in members]})


@members_bp.route('/projects/<int:project_id>/members', methods=['POST'])
@token_required
def add_member(project_id):
    membership = ProjectMember.query.filter_by(
        project_id=project_id, user_id=g.current_user.id
    ).first()
    if not membership or membership.role != 'admin':
        return jsonify({'error': 'Only admins can add members'}), 403

    data = request.get_json()
    if not data or not data.get('email'):
        return jsonify({'error': 'Email is required'}), 400

    user = User.query.filter_by(email=data['email'].lower().strip()).first()
    if not user:
        return jsonify({'error': 'User not found with this email'}), 404

    existing = ProjectMember.query.filter_by(
        project_id=project_id, user_id=user.id
    ).first()
    if existing:
        return jsonify({'error': 'User is already a member'}), 409

    member = ProjectMember(
        project_id=project_id,
        user_id=user.id,
        role=data.get('role', 'member')
    )
    db.session.add(member)
    db.session.commit()

    return jsonify({'member': member.to_dict(), 'message': 'Member added'}), 201


@members_bp.route('/projects/<int:project_id>/members/<int:user_id>', methods=['PUT'])
@token_required
def update_member_role(project_id, user_id):
    membership = ProjectMember.query.filter_by(
        project_id=project_id, user_id=g.current_user.id
    ).first()
    if not membership or membership.role != 'admin':
        return jsonify({'error': 'Only admins can change roles'}), 403

    target = ProjectMember.query.filter_by(
        project_id=project_id, user_id=user_id
    ).first()
    if not target:
        return jsonify({'error': 'Member not found'}), 404

    data = request.get_json()
    if not data or data.get('role') not in ['admin', 'member']:
        return jsonify({'error': 'Valid role (admin/member) is required'}), 400

    target.role = data['role']
    db.session.commit()

    return jsonify({'member': target.to_dict(), 'message': 'Role updated'})


@members_bp.route('/projects/<int:project_id>/members/<int:user_id>', methods=['DELETE'])
@token_required
def remove_member(project_id, user_id):
    membership = ProjectMember.query.filter_by(
        project_id=project_id, user_id=g.current_user.id
    ).first()
    if not membership or membership.role != 'admin':
        return jsonify({'error': 'Only admins can remove members'}), 403

    if user_id == g.current_user.id:
        admin_count = ProjectMember.query.filter_by(
            project_id=project_id, role='admin'
        ).count()
        if admin_count <= 1:
            return jsonify({'error': 'Cannot remove the only admin'}), 400

    target = ProjectMember.query.filter_by(
        project_id=project_id, user_id=user_id
    ).first()
    if not target:
        return jsonify({'error': 'Member not found'}), 404

    db.session.delete(target)
    db.session.commit()

    return jsonify({'message': 'Member removed successfully'})
