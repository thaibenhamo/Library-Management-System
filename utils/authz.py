from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt() or {}
            if claims.get("role") not in roles:
                return jsonify({"error": "forbidden", "required_role": roles}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
