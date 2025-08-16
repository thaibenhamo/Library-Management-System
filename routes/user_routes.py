from flask import Blueprint, request, jsonify
from services.user_service import UserService
from flask_jwt_extended import create_access_token

user_bp = Blueprint('user_bp', __name__)
user_service = UserService()


@user_bp.route('', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    if not data.get('username'):
        return jsonify({'error': 'Username is required'}), 400
    if not data.get('password'):
        return jsonify({'error': 'Password is required'}), 400

    user, error = user_service.create_user(
        username=data['username'],
        password=data['password'],
        email=data.get('email')
    )
    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201


@user_bp.route('', methods=['GET'])
def get_all_users():
    users = user_service.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route('/username/<string:username>', methods=['GET'])
def get_user_by_username(username):
    user = user_service.get_user_by_username(username)
    if not user:
        return jsonify({'error': 'User not found by username'}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route('/email/<string:email>', methods=['GET'])
def get_user_by_email(email):
    user = user_service.get_user_by_email(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success, message = user_service.delete_user(user_id)
    if not success:
        return jsonify({'message': message}), 404
    # 204 must not include a body
    return '', 204

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user, error = user_service.authenticate_user(username, password)
    if error:
        return jsonify({'error': error}), 401

    access_token = create_access_token(identity=user.id)  # Store user.id in the token

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    updated_user, error = user_service.update_user(user_id, data)
    if error:
        return jsonify({'error': error}), 400

    return jsonify(updated_user.json()), 200
