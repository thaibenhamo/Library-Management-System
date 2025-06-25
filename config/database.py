from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import environ

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()


def init_db(app):
    """Initialize database with app context"""
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all() 