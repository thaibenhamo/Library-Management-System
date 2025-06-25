from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_bp = Blueprint('user_bp', __name__)
user_service = UserService()


@user_bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400
    
    # Create user using service
    user, error = user_service.create_user(
        username=data['username'],
        password=data['password'],
        email=data.get('email')
    )
    
    if error:
        return jsonify({'message': error}), 409 if "already exists" in error else 500
    
    return jsonify({
        'message': 'User created successfully',
        'user': user.json()
    }), 201


@user_bp.route('/', methods=['GET'])
def get_all_users():
    users = user_service.get_all_users()
    return jsonify([user.json() for user in users]), 200


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user.json()), 200


@user_bp.route('/username/<string:username>', methods=['GET'])
def get_user_by_username(username):
    user = user_service.get_user_by_username(username)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user.json()), 200


@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success, message = user_service.delete_user(user_id)
    
    if not success:
        return jsonify({'message': message}), 404
    
    return jsonify({'message': 'User deleted successfully'}), 200

