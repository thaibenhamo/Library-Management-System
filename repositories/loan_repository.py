from models.loan_model import Loan
from extensions import db


class LoanRepository:
    def __init__(self, db_session=None):
        self.db_session = db_session or db.session

    def get_all(self):
        """Get all loans"""
        try:
            return self.db_session.query(Loan).all()
        except Exception as e:
            print(f"Error fetching all loans: {e}")
            return []

    def create(self, loan_data):
        """Create a new loan"""
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
        """Get all active (non-returned) loans"""
        try:
            return self.db_session.query(Loan).filter(Loan.is_returned == False).all()
        except Exception as e:
            print(f"Error fetching active loans: {e}")
            return []

    def get_by_id(self, loan_id):
        return self.db_session.get(Loan, loan_id)

    def update(self, loan):
        try:
            self.db_session.commit()
            return True
        except Exception as e:
            self.db_session.rollback()
            print(f"Error updating loan: {e}")
            return False

    def get_by_user_id(self, user_id):
        return self.db_session.query(Loan).filter_by(user_id=user_id).all()

