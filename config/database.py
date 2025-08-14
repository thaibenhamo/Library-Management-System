from os import environ, makedirs
from os.path import join
from extensions import db, bcrypt
# Singletons


def init_db(app):
    # Keep DB in instance/app.db so path is deterministic
    makedirs(app.instance_path, exist_ok=True)
    db_path = join(app.instance_path, "app.db")

    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL', f'sqlite:///{db_path}')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        # IMPORTANT: import models BEFORE create_all
        from models.user_model import User  # add more models here later
        db.create_all()
        create_default_admin()


def create_default_admin():
    """Create default admin user if none exists"""
    from models.user_model import User
    from utils.password_utils import hash_password

    # Check if any admin user exists
    admin_exists = User.query.filter_by(role='admin').first()

    if not admin_exists:
        admin_password = hash_password('admin123')  # Default password
        admin_user = User(
            username='admin',
            email='admin@library.com',
            password=admin_password,
            role='admin',
            is_active=True
        )

        db.session.add(admin_user)
        db.session.commit()

        print("Default admin user created!")
        print("Username: admin")
        print("Password: admin123")
