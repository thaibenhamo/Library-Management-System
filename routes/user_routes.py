from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_bp = Blueprint('user_bp', __name__)
user_service = UserService()


@user_bp.route('', methods=['POST'])
def add_user():
    """
    Create a new user.

    Args:
        JSON body: {'username': str, 'password': str, 'email': str}

    Returns:
        201: User created successfully.
        400: Missing required fields or validation error.
    """
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
    """
    Get all users.

    Returns:
        200: List of all users.
    """
    users = user_service.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a specific user by ID.

    Args:
        user_id (int): User ID from URL path.

    Returns:
        200: User details.
        404: User not found.
    """
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route('/username/<string:username>', methods=['GET'])
def get_user_by_username(username):
    """
    Get a user by username.

    Args:
        username (str): Username from URL path.

    Returns:
        200: User details.
        404: User not found.
    """
    user = user_service.get_user_by_username(username)
    if not user:
        return jsonify({'error': 'User not found by username'}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route('/email/<string:email>', methods=['GET'])
def get_user_by_email(email):
    """
    Get a user by email address.

    Args:
        email (str): Email address from URL path.

    Returns:
        200: User details.
        404: User not found.
    """
    user = user_service.get_user_by_email(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user by ID.

    Args:
        user_id (int): User ID from URL path.

    Returns:
        204: User deleted successfully.
        404: User not found.
    """
    success, message = user_service.delete_user(user_id)
    if not success:
        return jsonify({'message': message}), 404

    return '', 204


@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update an existing user.

    Args:
        user_id (int): User ID from URL path.
        JSON body: Fields to update (e.g., 'username', 'email', 'password').

    Returns:
        200: User updated successfully.
        400: Missing data or validation error.
        404: User not found.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    updated_user, error = user_service.update_user(user_id, data)
    if error:
        if error == "User not found":
            return jsonify({'error': error}), 404
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'User updated successfully',
        'user': updated_user.to_dict()
    }), 200
