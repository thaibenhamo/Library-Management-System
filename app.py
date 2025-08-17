from flask import Flask, jsonify

from config import Config
from app_config.database import init_db
from extensions import jwt

from routes.auth_routes import auth_bp
from routes.health_routes import health_bp
from routes.user_routes import user_bp
from routes.author_routes import author_bp
from routes.book_routes import book_bp
from routes.category_routes import category_bp
from routes.book_copy_routes import book_copy_bp
from routes.loan_routes import loan_bp
from routes.export_routes import export_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)
    jwt.init_app(app)

    @app.errorhandler(Exception)
    def handle_error(err):
        code = getattr(err, "code", 500)
        return jsonify({"error": type(err).__name__, "message": str(err)}), code

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(author_bp, url_prefix='/api/authors')
    app.register_blueprint(book_bp, url_prefix='/api/books')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.register_blueprint(book_copy_bp, url_prefix="/api/book_copies")
    app.register_blueprint(loan_bp, url_prefix="/api/loans")
    app.register_blueprint(export_bp, url_prefix="/api/export")

    return app


if __name__ == '__main__':
    
    app = create_app()
    app.run(debug=True)