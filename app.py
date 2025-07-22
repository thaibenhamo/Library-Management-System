from flask import Flask
from config.database import init_db
from routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    
    # Initialize database
    init_db(app)

    # Register Blueprints
    app.register_blueprint(user_bp, url_prefix='/api/users')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
