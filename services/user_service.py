from models.user_model import User
from repositories.user_repository import UserRepository
import re


class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()
    
    def create_user(self, username, password, email=None):
        """
        Create a new user
        """
        username_pattern = r"^[0-9A-Za-z]{6,16}$"
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,32}$"

        if re.match(username_pattern, username):
            return None, "Invalid username format"

        if re.match(password_pattern, password):
            return None, ("Password must be 8-32 characters long and include uppercase, lowercase, digit, "
                          "and special character")

        if email and not re.match(email_pattern, email):
            return None, "Invalid email format"

        if self.user_repository.find_by_username(username):
            return None, "Username already exists"

        if self.user_repository.find_by_email(email):
            return None, "Email already exists"

        new_user = User(username=username, password=password, email=email)

        return self.user_repository.save(new_user)
    
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
