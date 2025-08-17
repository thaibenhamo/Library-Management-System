"""
Service layer for user-related operations.
Handles user creation, validation, retrieval, authentication, and updates.
"""

import re
from models.user_model import User
from repositories.user_repository import UserRepository
from utils.password_utils import hash_password
from werkzeug.security import check_password_hash  # required for authenticate_user

class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def create_user(self, username, password, email=None):
        """
        Create a new user after validating username, email, and password formats.

        Args:
            username (str): Desired username (6–16 alphanumeric characters).
            password (str): Password (8–32 characters, must include lowercase, uppercase, digit, and special char).
            email (str, optional): Valid email address.

        Returns:
            tuple[User | None, str | None]: Created user object or error message.
        """
        username_re = r"^[A-Za-z][a-zA-Z0-9_]{2,15}$"
        email_re = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        password_re = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,32}$"

        if not re.fullmatch(username_re, username):
            return None, ("Username must start with a letter, can contain letters, numbers and underscores "
                          "(3–16  characters).")
        if not re.fullmatch(email_re, email):
            return None, "Invalid email format."
        if not re.fullmatch(password_re, password):
            return None, ("Password must be 8–32 chars with at least one lowercase, "
                          "one uppercase, one digit, and one special char.")

        if self.user_repository.find_by_username(username):
            return None, "Username already taken."
        if email and self.user_repository.find_by_email(email):
            return None, "Email already in use."

        hashed_password = hash_password(password)
        user = User(username=username, password=hashed_password, email=email)
        return self.user_repository.save(user)

    def get_user_by_id(self, user_id):
        """
        Retrieve user by their ID.

        Args:
            user_id (int): User ID.

        Returns:
            User | None
        """
        return self.user_repository.find_by_id(user_id)

    def get_user_by_email(self, email):
        """
        Retrieve user by email.

        Args:
            email (str): User's email address.

        Returns:
            User | None
        """
        return self.user_repository.find_by_email(email)

    def get_user_by_username(self, username):
        """
        Retrieve user by username.

        Args:
            username (str): Username.

        Returns:
            User | None
        """
        return self.user_repository.find_by_username(username)

    def get_all_users(self):
        """
        Retrieve all users in the system.

        Returns:
            list[User]
        """
        return self.user_repository.find_all()

    def delete_user(self, user_id):
        """
        Delete a user by their ID.

        Args:
            user_id (int): User ID.

        Returns:
            tuple[bool, str | None]: Success status and error message if failed.
        """
        user = self.user_repository.find_by_id(user_id)
        if not user:
            return False, "User not found"

        return self.user_repository.delete(user)

    def authenticate_user(self, username, password):
        """
        Validate user credentials.

        Args:
            username (str): Username.
            password (str): Raw password.

        Returns:
            tuple[User | None, str | None]: Authenticated user or error message.
        """
        user = self.user_repository.find_by_username(username)
        if user and check_password_hash(user.password, password):
            return user, None
        return None, "Invalid credentials"

    def update_user(self, user_id, data):
        """
        Update fields of an existing user.

        Args:
            user_id (int): User ID.
            data (dict): Fields to update (e.g., 'username', 'email').

        Returns:
            tuple[User | None, str | None]: Updated user or error message.
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None, "User not found"

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']

        try:
            self.user_repository.save(user)
            return user, None
        except Exception as e:
            return None, str(e)
