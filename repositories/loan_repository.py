from models.loan_model import Loan
from extensions import db


class LoanRepository:
    """
    Repository class for managing Loan database operations with error handling.

    Provides CRUD operations, query methods, and statistical functions for Loan model instances,
    including active loan tracking and user-specific queries.

    Args:
        db_session (Session, optional): Database session instance, defaults to db.session.

    Attributes:
        db_session (Session): Database session for executing queries.

    Returns:
        LoanRepository: Repository instance for Loan operations.
    """
    def __init__(self, db_session=None):
        """
        Initialize repository with database session.

        Args:
            db_session (Session, optional): Custom database session, defaults to db.session.
        """
        self.db_session = db_session or db.session

    def get_all(self):
        """
        Retrieve all loans from the database with error handling.

        Returns:
            list[Loan]: List of all Loan instances, empty list on error.
        """
        try:
            return self.db_session.query(Loan).all()
        except Exception as e:
            print(f"Error fetching all loans: {e}")
            return []

    def create(self, loan_data):
        """
        Create new loan from dictionary data with transaction management.

        Args:
            loan_data (dict): Dictionary containing loan attributes.

        Returns:
            Loan or None: Created loan instance on success, None on failure.
        """
        try:
            loan = Loan(**loan_data)
            self.db_session.add(loan)
            self.db_session.commit()
            return loan
        except Exception as e:
            self.db_session.rollback()
            print(f"Error creating loan: {e}")
            return None

    def get_active_loans(self):
        """
        Retrieve all active (non-returned) loans with error handling.

        Returns:
            list[Loan]: List of Loan instances where is_returned=False, empty list on error.
        """
        try:
            return self.db_session.query(Loan).filter(Loan.is_returned == False).all()
        except Exception as e:
            print(f"Error fetching active loans: {e}")
            return []

    def get_by_id(self, loan_id):
        """
        Retrieve loan by ID from the database.

        Args:
            loan_id (int): Primary key ID of the loan.

        Returns:
            Loan or None: Loan instance if found, None otherwise.
        """
        return self.db_session.get(Loan, loan_id)

    def update(self, loan):
        """
        Commit changes to existing loan with rollback on error.

        Args:
            loan (Loan): Modified Loan instance to update.

        Returns:
            bool: True if update successful, False on failure.
        """
        try:
            self.db_session.commit()
            return True
        except Exception as e:
            self.db_session.rollback()
            print(f"Error updating loan: {e}")
            return False

    def get_by_user_id(self, user_id):
        """
        Retrieve all loans for a specific user.

        Args:
            user_id (int): User ID to filter loans by.

        Returns:
            list[Loan]: List of Loan instances for the specified user.
        """
        return self.db_session.query(Loan).filter_by(user_id=user_id).all()

    def count_all_loans(self):
        """
        Get total count of all loans in the database.

        Returns:
            int: Total number of loan records.
        """
        return self.db_session.query(Loan).count()

    def count_loans_by_return_status(self, returned=True):
        """
        Count loans by return status for statistical reporting.

        Args:
            returned (bool): Return status to count, defaults to True.

        Returns:
            int: Number of loans matching the specified return status.
        """
        return self.db_session.query(Loan).filter_by(is_returned=returned).count()
