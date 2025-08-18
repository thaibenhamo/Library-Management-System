from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, BadRequest

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
    """
    Application factory function to create and configure Flask app.

    Sets up database, JWT authentication, error handling, and registers
    all API blueprints with their respective URL prefixes.

    Returns:
        Flask: Configured Flask application instance ready to run.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)
    jwt.init_app(app)

    @app.errorhandler(Exception)
    def handle_error(err):
        """
        Global error handler for all exceptions.

        Provides consistent JSON error responses across the application.
        Distinguishes between HTTP errors and unexpected server errors.

        Args:
            err (Exception): The caught exception.

        Returns:
            tuple: JSON response and HTTP status code.
                  Format: {"error": "ErrorType", "message": "description"}
        """
        if isinstance(err, HTTPException):
            code = err.code
            if isinstance(err, BadRequest):
                message = "Invalid request payload"  # safer message
            else:
                message = err.description
        else:
            code = 500
            message = "An unexpected error occurred"

        return jsonify({
            "error": type(err).__name__,
            "message": message
        }), code

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
    """
    Entry point for running the application directly.

    Creates the Flask app using the factory pattern and starts
    the development server with debug mode enabled.
    """
    app = create_app()
    app.run(debug=True)