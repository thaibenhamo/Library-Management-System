from services.user_service import UserService
from utils.password_utils import check_password
import logging


class AuthService:
    """
    Service class responsible for authentication and logout logging.

    This class interacts with the UserService to validate user credentials,
    manage authentication flows, and record login/logout activities.
    """

    def __init__(self):
        """
        Initialize AuthService with an instance of UserService.
        """
        self.user_service = UserService()

    def authenticate(self, username, password):
        """
        Authenticate a user by verifying username and password.

        Args:
            username (str): The username of the user attempting to log in.
            password (str): The plaintext password provided by the user.

        Returns:
            tuple:
                - user (User | None): The authenticated user object if valid,
                  otherwise None.
                - error (str | None): Error message if authentication failed,
                  otherwise None.
        """
        user = self.user_service.get_user_by_username(username)
        if not user:
            logging.warning(f"Failed login attempt - user not found: {username}")
            return None, "Invalid username or password"

        if not check_password(user.password, password):
            logging.warning(f"Failed login attempt - wrong password: {username}")
            return None, "Invalid username or password"

        if not user.is_active:
            return None, "Account is deactivated"

        logging.info(f"Successful authentication for user: {username}")
        return user, None

    def log_logout(self, user_id):
        """
        Record a logout event for the given user.

        Args:
            user_id (int): ID of the user who is logging out.
        """
        try:
            user = self.user_service.get_user_by_id(user_id)
            if user:
                logging.info(f"User {user.username} logged out")
        except Exception as e:
            logging.error(f"Logout logging error: {str(e)}")



