from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def role_required(*roles):
    """
    Decorator to restrict access to routes based on user roles.

    Verifies JWT token and checks if user's role matches any of the required roles.
    Returns 403 Forbidden if the user's role is not in the allowed roles list.

    Args:
        *roles (str): Variable number of allowed roles (e.g., 'admin', 'member', 'moderator').

    Returns:
        function: Decorated function that enforces role-based access control.

    Raises:
        403: If user's role is not in the required roles list.
        401: If JWT token is invalid or missing (from verify_jwt_in_request).
    """
    def decorator(fn):
        """
        Inner decorator that wraps the target function.

        Args:
            fn (function): The route function to be decorated.

        Returns:
            function: Wrapped function with role checking.
        """
        @wraps(fn)
        def wrapper(*args, **kwargs):
            """
            Wrapper function that performs JWT verification and role validation.

            Args:
                *args: Positional arguments passed to the original function.
                **kwargs: Keyword arguments passed to the original function.

            Returns:
                Response: 403 Forbidden if role doesn't match, otherwise calls original function.
            """
            verify_jwt_in_request()
            claims = get_jwt() or {}
            if claims.get("role") not in roles:
                return jsonify({"error": "forbidden", "required_role": roles}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
