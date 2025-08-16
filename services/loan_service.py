from repositories.loan_repository import LoanRepository
from repositories.book_copy_repository import BookCopyRepository
from repositories.user_repository import UserRepository
from datetime import date, timedelta


class LoanService:
    def __init__(self):
        self.loan_repo = LoanRepository()
        self.book_copy_repo = BookCopyRepository()
        self.user_repo = UserRepository()

    def get_loans_by_user(self, user_id):
        """Get all loans for a specific user"""
        loans = self.loan_repo.get_by_user_id(user_id)
        return [loan.json() for loan in loans]

    def create_loan(self, loan_data):
        """Create a new loan"""
        if 'loan_date' not in loan_data or loan_data['loan_date'] is None:
            loan_data['loan_date'] = date.today()

        if 'return_date' not in loan_data or loan_data['return_date'] is None:
            loan_data['return_date'] = date.today() + timedelta(days=14)

        # Validate book_copy exists
        book_copy = self.book_copy_repo.get_by_id(loan_data['book_copy_id'])
        if not book_copy:
            return None, "Book copy does not exist"

        # Validate user exists
        user = self.user_repo.find_by_id(loan_data['user_id'])
        if not user:
            return None, "User does not exist"

        # Check if already loaned
        active_loans = self.loan_repo.get_active_loans()
        for loan in active_loans:
            if loan.book_copy_id == loan_data.get('book_copy_id'):
                return None, "Book is already on loan"

        loan = self.loan_repo.create(loan_data)
        if loan:
            return loan.json(), None
        return None, "Failed to create loan"

    def return_loan(self, loan_id, user_id):
        """Return a loaned book, only if the loan belongs to the user"""
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
        """Get a loan by ID, but only if it belongs to the current user"""
        loan = self.loan_repo.get_by_id(loan_id)
        if not loan:
            return None, "Loan not found"
        if loan.user_id != user_id:
            return None, "Unauthorized"
        return loan.json(), None

    def get_loan_statistics(self):
        total = self.loan_repo.count_all_loans()
        returned = self.loan_repo.count_loans_by_return_status(True)
        not_returned = self.loan_repo.count_loans_by_return_status(False)

        return {
            'total_loans': total,
            'returned_loans': returned,
            'not_returned_loans': not_returned
        }




