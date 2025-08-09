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
