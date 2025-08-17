from repositories.loan_repository import LoanRepository
from repositories.book_copy_repository import BookCopyRepository
from repositories.user_repository import UserRepository
from datetime import date, timedelta


class LoanService:
    """
    Service for business logic related to book loans.

    Attributes:
        loan_repo (LoanRepository): Repository for loan persistence.
        book_copy_repo (BookCopyRepository): Repository for book copy queries.
        user_repo (UserRepository): Repository for user validation.
    """
    def __init__(self):
        """
        Initialize service with repository dependencies.
        """
        self.loan_repo = LoanRepository()
        self.book_copy_repo = BookCopyRepository()
        self.user_repo = UserRepository()

    def get_loans_by_user(self, user_id):
        """
        Retrieve all loans made by a specific user.

        Args:
            user_id (int): ID of the user.

        Returns:
            list[dict]: List of loan records in JSON format.
        """
        loans = self.loan_repo.get_by_user_id(user_id)
        return [loan.json() for loan in loans]

    def create_loan(self, loan_data):
        """
        Create a new loan if the book copy is available and user exists.

        Args:
            loan_data (dict): Dictionary with keys: user_id, book_copy_id, loan_date (optional), return_date (optional).

        Returns:
            tuple[dict, str]: (loan JSON, error message) — returns error message if failed.
        """
        if 'loan_date' not in loan_data or loan_data['loan_date'] is None:
            loan_data['loan_date'] = date.today()

        if 'return_date' not in loan_data or loan_data['return_date'] is None:
            loan_data['return_date'] = date.today() + timedelta(days=14)

        book_copy = self.book_copy_repo.get_by_id(loan_data['book_copy_id'])
        if not book_copy:
            return None, "Book copy does not exist"

        user = self.user_repo.find_by_id(loan_data['user_id'])
        if not user:
            return None, "User does not exist"

        # Check if book copy is already on loan
        for loan in self.loan_repo.get_active_loans():
            if loan.book_copy_id == loan_data.get('book_copy_id'):
                return None, "Book is already on loan"

        loan = self.loan_repo.create(loan_data)
        if loan:
            return loan.json(), None
        return None, "Failed to create loan"

    def return_loan(self, loan_id, user_id):
        """
        Mark a loan as returned (only if owned by the user).

        Args:
            loan_id (int): ID of the loan.
            user_id (int): ID of the user performing the return.

        Returns:
            tuple[dict, str]: (updated loan JSON, error message) — returns error message if failed.
        """
        loan = self.loan_repo.get_by_id(loan_id)
        if not loan:
            return None, "Loan not found"
        if loan.user_id != user_id:
            return None, "Unauthorized access to this loan"
        if loan.is_returned:
            return None, "Book already returned"

        loan.is_returned = True
        if loan.book_copy:
            loan.book_copy.available = True

        success = self.loan_repo.update(loan)
        if not success:
            return None, "Failed to return book"

        return loan.json(), None

    def get_loan_by_id_for_user(self, loan_id, user_id):
        """
        Fetch a specific loan by ID if it belongs to the user.

        Args:
            loan_id (int): Loan ID.
            user_id (int): User ID.

        Returns:
            tuple[dict, str]: (loan JSON, error message)
        """
        loan = self.loan_repo.get_by_id(loan_id)
        if not loan:
            return None, "Loan not found"
        if loan.user_id != user_id:
            return None, "Unauthorized"
        return loan.json(), None

    def get_loan_statistics(self):
        """
        Get statistics for all loan records.

        Returns:
            dict: Dictionary with counts for total, returned, and not returned loans.
        """
        total = self.loan_repo.count_all_loans()
        returned = self.loan_repo.count_loans_by_return_status(True)
        not_returned = self.loan_repo.count_loans_by_return_status(False)

        return {
            'total_loans': total,
            'returned_loans': returned,
            'not_returned_loans': not_returned
        }
