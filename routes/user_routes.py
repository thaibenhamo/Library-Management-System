from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_bp = Blueprint('user_bp', __name__)
user_service = UserService()


@user_bp.route('', methods=['POST'])
def add_user():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    required_fields = ['username', 'password', 'email']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    user, error = user_service.create_user(
        username=data['username'],
        password=data['password'],
        email=data['email']
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

    return '', 204


@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    updated_user, error = user_service.update_user(user_id, data)
    if error:
        if error == "User not found":
            return jsonify({'error': error}), 404
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Book updated successfully',
        'user': updated_user.to_dict()
    }), 200
