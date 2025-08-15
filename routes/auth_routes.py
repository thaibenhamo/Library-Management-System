from datetime import timedelta

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

from services.auth_service import AuthService
import logging

auth_bp = Blueprint('auth_bp', __name__)
auth_service = AuthService()


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        user, error = auth_service.authenticate(username, password)
        if error:
            return jsonify({'error': error}), 401

        additional_claims = {
            "role": user.role,
            "user_id": user.id
        }

        expires_delta = timedelta(hours=2)
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims,
            expires_delta=expires_delta
        )

        return jsonify({
            'access_token': access_token,
            'expires_in': int(expires_delta.total_seconds()),
            'user': {
                'id': user.id,
                'role': user.role
            }
        }), 200

    except Exception as e:
        logging.error(f"Login endpoint error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Simple logout - returns success message
    """
    try:
        current_user_id = get_jwt_identity()
        auth_service.log_logout(current_user_id)

        return jsonify({
            'message': 'Logged out successfully',
            'success': True
        }), 200

    except Exception as e:
        logging.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500
