from flask import Blueprint, jsonify

health_bp = Blueprint("health_bp", __name__)


@health_bp.get("/health")
def health():
    """
    Health check endpoint to verify service status.

    Returns:
        200: Service is healthy and operational.
    """
    return jsonify({"status": "ok"}), 200
