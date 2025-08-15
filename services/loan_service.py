from repositories.loan_repository import LoanRepository
from repositories.book_copy_repository import BookCopyRepository
from repositories.user_repository import UserRepository
from datetime import date, timedelta


class LoanService:
    def __init__(self):
        self.loan_repo = LoanRepository()
        self.book_copy_repo = BookCopyRepository()
        self.user_repo = UserRepository()

    def get_all_loans(self):
        """Get all loans"""
        loans = self.loan_repo.get_all()
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
                return None, "Book copy is already on loan"

        loan = self.loan_repo.create(loan_data)
        if loan:
            return loan.json(), None
        return None, "Failed to create loan"

    def return_loan(self, loan_id):
        loan = self.loan_repo.get_by_id(loan_id)

        if not loan:
            return None, "Loan not found"

        if loan.is_returned:
            return None, "Book already returned"

        loan.is_returned = True
        if loan.book_copy:
            loan.book_copy.available = True

        success = self.loan_repo.update(loan)
        if not success:
            return None, "Failed to return book"

        return loan.json(), None


    def get_loan_by_id(self, loan_id):
        loan = self.loan_repo.get_by_id(loan_id)
        if loan:
            return loan.json()
        return None



