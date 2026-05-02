from flask import Blueprint, request, jsonify, g
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from models import db, User
from middleware import token_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Name, email, and password are required'}), 400

    if User.query.filter_by(email=data['email'].lower().strip()).first():
        return jsonify({'error': 'Email already registered'}), 409

    if len(data['password']) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    password_hash = bcrypt.hashpw(
        data['password'].encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    user = User(
        name=data['name'].strip(),
        email=data['email'].lower().strip(),
        password_hash=password_hash,
        role=data.get('role', 'member')
    )

    db.session.add(user)
    db.session.commit()

    token = _generate_token(user.id)

    return jsonify({
        'message': 'Registration successful',
        'token': token,
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email'].lower().strip()).first()

    if not user or not bcrypt.checkpw(
        data['password'].encode('utf-8'),
        user.password_hash.encode('utf-8')
    ):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = _generate_token(user.id)

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    })


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_me():
    return jsonify({'user': g.current_user.to_dict()})


def _generate_token(user_id):
    secret = os.environ.get('JWT_SECRET', 'dev-secret-key-change-in-production')
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, secret, algorithm='HS256')
