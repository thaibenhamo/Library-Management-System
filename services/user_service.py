from models.user_model import User
from repositories.user_repository import UserRepository
import re
from utils.password_utils import hash_password


class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()
    
    def create_user(self, username, password, email=None):
        """
        Create a new user
        """
        username_re = r"^[A-Za-z0-9]{6,16}$"
        email_re = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        password_re = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,32}$"

        if not re.fullmatch(username_re, username):
            return None, "Invalid username format (6–16 alphanumerics)."
        if email and not re.fullmatch(email_re, email):
            return None, "Invalid email format."
        if not re.fullmatch(password_re, password):
            return None, ("Password must be 8–32 chars with at least one lowercase, "
                          "one uppercase, one digit, and one special char.")

        # Uniqueness checks
        if self.user_repository.find_by_username(username):
            return None, "Username already taken."
        if email and self.user_repository.find_by_email(email):
            return None, "Email already in use."
        hashed_password = hash_password(password)

        user = User(username=username, password=hashed_password, email=email)
        return self.user_repository.save(user)
    
    def get_user_by_id(self, user_id):
        """
        Get a user by ID
        """
        return self.user_repository.find_by_id(user_id)

    def get_user_by_email(self, email):
        """
        Get a user by email
        """
        return self.user_repository.find_by_email(email)

    def get_user_by_username(self, username):
        """
        Get a user by username
        """
        return self.user_repository.find_by_username(username)
    
    def get_all_users(self):
        """
        Get all users
        """
        return self.user_repository.find_all()
    
    def delete_user(self, user_id):
        """
        Delete a user by ID
        """
        user = self.user_repository.find_by_id(user_id)
        if not user:
            return False, "User not found"
        
        return self.user_repository.delete(user)

    def authenticate_user(self, username, password):
        user = self.user_repository.find_by_username(username)
        if user and check_password_hash(user.password, password):
            return user, None
        return None, "Invalid credentials"

    def update_user(self, user_id, data):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None, "User not found"

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        # Add more fields as needed

        try:
            self.user_repository.save(user)
            return user, None
        except Exception as e:
            return None, str(e)
