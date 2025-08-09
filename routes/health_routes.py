from flask import Blueprint, jsonify

health_bp = Blueprint("health_bp", __name__)

@health_bp.get("/health")
def health():
    return jsonify({"status": "ok"}), 200
