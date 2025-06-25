from config.database import db
from utils.password_utils import hash_password


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, username, password, email=None):
        self.username = username
        self.password = hash_password(password)
        self.email = email

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }