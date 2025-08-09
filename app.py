from flask import Flask, jsonify
from config.database import init_db
from extensions import jwt, limiter, cache
from routes.health_routes import health_bp

def create_app():
    app = Flask(__name__)

    # temporary secret; we’ll move this to env later
    app.config["JWT_SECRET_KEY"] = "change-me"

    init_db(app)
    jwt.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    @app.errorhandler(Exception)
    def handle_error(err):
        code = getattr(err, "code", 500)
        return jsonify({"error": type(err).__name__, "message": str(err)}), code

    app.register_blueprint(health_bp, url_prefix="/api")
    return app

app = create_app()
