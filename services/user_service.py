from models.user_model import User
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()
    
    def create_user(self, username, password, email=None):
        """
        Create a new user
        """
        # Check if user already exists
        if self.user_repository.find_by_username(username):
            return None, "Username already exists"
        
        # Check if email exists and is unique
        if email and self.user_repository.find_by_email(email):
            return None, "Email already exists"
        
        # Create new user
        new_user = User(
            username=username,
            password=password,
            email=email
        )
        
        # Save to database using repository
        return self.user_repository.save(new_user)
    
    def get_user_by_id(self, user_id):
        """
        Get a user by ID
        """
        return self.user_repository.find_by_id(user_id)
    
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