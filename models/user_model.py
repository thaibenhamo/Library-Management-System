from extensions import db
from sqlalchemy import func


class User(db.Model):
    """
    User model for managing user accounts and authentication.

    Args:
        username (str): Unique username, max 80 characters.
        email (str): Unique email address, max 120 characters.
        password (str): Hashed password, max 255 characters.
        role (str, optional): User role, defaults to "member".
        is_active (bool, optional): Account status, defaults to True.

    Attributes:
        id (int): Auto-generated primary key.
        username (str): Unique username, max 80 characters, required.
        email (str): Unique email address, max 120 characters, required.
        password (str): Hashed password string, max 255 characters, required.
        role (str): User role (admin|librarian|member), defaults to "member".
        is_active (bool): Account active status, defaults to True.
        created_at (datetime): Account creation timestamp, auto-generated.

    Returns:
        User: User model instance.
    """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # hashed
    role = db.Column(db.String(20), default="member")     # admin|librarian|member
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=func.now())

    def to_dict(self):
        """
        Convert User object to dictionary format excluding sensitive data.

        Args:
            None

        Returns:
            dict: Dictionary containing user id, username, email, role, status, and creation timestamp.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
