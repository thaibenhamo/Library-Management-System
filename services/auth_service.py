from services.user_service import UserService
from utils.password_utils import check_password
import logging


class AuthService:
    def __init__(self):
        self.user_service = UserService()

    def authenticate(self, username, password):
        try:
            # Find user by username
            user = self.user_service.get_user_by_username(username)
            if not user:
                logging.warning(f"Failed login attempt - user not found: {username}")
                return None, "Invalid username or password"

            # Check password
            if not check_password(user.password, password):
                logging.warning(f"Failed login attempt - wrong password: {username}")
                return None, "Invalid username or password"

            # Check if user is active
            if not user.is_active:
                return None, "Account is deactivated"

            logging.info(f"Successful authentication for user: {username}")
            return user, None

        except Exception as e:
            logging.error(f"Authentication error: {str(e)}")
            return None, "Authentication failed"

    def log_logout(self, user_id):
        try:
            user = self.user_service.get_user_by_id(user_id)
            if user:
                logging.info(f"User {user.username} logged out")
        except Exception as e:
            logging.error(f"Logout logging error: {str(e)}")



