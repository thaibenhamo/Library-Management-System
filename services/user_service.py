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
    USERNAME_RE = r"^[A-Za-z][a-zA-Z0-9_]{2,15}$"
    EMAIL_RE = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    PASSWORD_RE = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,32}$"

    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def is_username_unique(self, username, exclude_user_id=None):
        """
        Check if username is unique.

        Returns tuple: (True, None) if unique, (False, error).
        """
        existing_user = self.user_repository.find_by_username(username)
        if not existing_user:
            return True, None
        if exclude_user_id and existing_user.id == exclude_user_id:
            return True, None
        return False, "Username already taken."

    def is_email_unique(self, email, exclude_user_id=None):
        """
        Check if email is unique. Returns tuple: (True, None) if unique, (False, error).
        """
        existing_user = self.user_repository.find_by_email(email)
        if not existing_user:
            return True, None
        if exclude_user_id and existing_user.id == exclude_user_id:
            return True, None
        return False, "Email already in use."

    @classmethod
    def validate_username(cls, username):
        """
        Validate username format.

        Args:
            username (str): Username to validate.

        Returns:
            tuple[bool, str | None]: Validation result and error message.
        """
        if not re.fullmatch(cls.USERNAME_RE, username):
            return False, ("Username must start with a letter and contain letters, numbers, "
                           "or underscores (3–16 characters).")
        return True, None

    @classmethod
    def validate_email(cls, email):
        """
        Validate email format using class regex pattern.

        Args:
            email (str): Email to validate.

        Returns:
            tuple[bool, str | None]: Validation result and error message.
        """
        if not re.fullmatch(cls.EMAIL_RE, email):
            return False, "Invalid email format."
        return True, None

    @classmethod
    def validate_password(cls, password):
        """
        Validate password format using class regex pattern.

        Args:
            password (str): Password to validate.

        Returns:
            tuple[bool, str | None]: Validation result and error message.
        """
        if not re.fullmatch(cls.PASSWORD_RE, password):
            return False, ("Password must be 8–32 characters and include at least one lowercase letter, "
                           "one uppercase letter, one digit, and one special character.")
        return True, None

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
        valid, error = UserService.validate_username(username)
        if not valid:
            return None, error

        valid, error = UserService.validate_email(email)
        if not valid:
            return None, error

        valid, error = UserService.validate_password(password)
        if not valid:
            return None, error

        ok, err = self.is_username_unique(username)
        if not ok:
            return None, err

        ok, err = self.is_email_unique(email)
        if not ok:
            return None, err

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
        user = self.user_repository.find_by_id(user_id)
        if not user:
            return None, "User not found"

        username = data.get('username')
        if username is not None:
            valid, error = UserService.validate_username(username)
            if not valid:
                return None, error
            ok, err = self.is_username_unique(username)
            if not ok:
                return None, err
            user.username = username

        email = data.get('email')
        if email is not None:
            valid, error = UserService.validate_email(email)
            if not valid:
                return None, error
            ok, err = self.is_email_unique(email)
            if not ok:
                return None, err
            user.email = email

        password = data.get('password')
        if password is not None:
            valid, error = UserService.validate_password(password)
            if not valid:
                return None, error
            user.password = hash_password(password)

        updated, error = self.user_repository.update(user)
        return (updated, None) if updated else (None, "Failed to update user")
