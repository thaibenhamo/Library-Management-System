from extensions import db
from models.user_model import User


class UserRepository:
    """
    Repository class for managing User database operations with comprehensive error handling.

    Provides CRUD operations, query methods, and partial update functionality for User model instances,
    including username and email-based searches with transaction management.

    Args:
        db_session (Session, optional): Database session instance, defaults to db.session.

    Attributes:
        db_session (Session): Database session for executing queries.

    Returns:
        UserRepository: Repository instance for User operations.
    """
    def __init__(self, db_session=None):
        """
        Initialize repository with database session.

        Args:
            db_session (Session, optional): Custom database session, defaults to db.session.

        Returns:
            None
        """
        self.db_session = db_session or db.session
    
    def save(self, user):
        """
        Save new user to database with transaction management.

        Args:
            user (User): User instance to save.

        Returns:
            tuple: (User, None) on success or (None, error_message) on failure.
        """
        try:
            self.db_session.add(user)
            self.db_session.commit()
            return user, None
        except Exception as e:
            self.db_session.rollback()
            return None, str(e)

    def find_by_id(self, user_id):
        """
        Retrieve user by ID from the database.

        Args:
            user_id (int): Primary key ID of the user.

        Returns:
            User or None: User instance if found, None otherwise.
        """
        return self.db_session.get(User, user_id)

    def find_by_username(self, username):
        """
        Retrieve user by username using SQLAlchemy select statement.

        Args:
            username (str): Username to search for.

        Returns:
            User or None: User instance if found, None otherwise.
        """
        stmt = db.select(User).where(User.username == username)
        return self.db_session.scalars(stmt).first()
    
    def find_by_email(self, email):
        """
        Retrieve user by email address using SQLAlchemy select statement.

        Args:
            email (str): Email address to search for.

        Returns:
            User or None: User instance if found, None otherwise.
        """
        stmt = db.select(User).where(User.email == email)
        return self.db_session.scalars(stmt).first()
    
    def find_all(self):
        """
        Retrieve all users from the database using SQLAlchemy select statement.

        Args:
            None

        Returns:
            list[User]: List of all User instances.
        """
        stmt = db.select(User)
        return self.db_session.scalars(stmt).all()
    
    def delete(self, user):
        """
        Delete user from database with transaction management.

        Args:
            user (User): User instance to delete.

        Returns:
            tuple: (True, None) on success or (False, error_message) on failure.
        """
        try:
            self.db_session.delete(user)
            self.db_session.commit()
            return True, None
        except Exception as e:
            self.db_session.rollback()
            return False, str(e)

    def update(self, user: User, **fields):
        """
        Update specified fields of an existing user and commit the transaction.

        Args:
            user (User): The user instance to update.
            **fields: Arbitrary keyword arguments representing fields to update
                     (e.g. username='newname', email='newemail@example.com').

        Returns:
            tuple[User | None, str | None]:
                On success: (updated User instance, None)
                On failure: (None, error message as str)
        """
        try:
            for k, v in fields.items():
                setattr(user, k, v)
            self.db_session.commit()
            return user, None
        except Exception as e:
            self.db_session.rollback()
            return None, str(e)
