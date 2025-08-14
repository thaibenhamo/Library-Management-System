from repositories.loan_repository import LoanRepository
from datetime import date, timedelta


class LoanService:
    def __init__(self):
        self.loan_repo = LoanRepository()

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

        active_loans = self.loan_repo.get_active_loans()
        for loan in active_loans:
            if loan.book_copy_id == loan_data.get('book__copy_id'):
                return None, "Book copy is already on loan"

        loan = self.loan_repo.create(loan_data)
        if loan:
            return loan.json(), None
        return None, "Failed to create loan"
