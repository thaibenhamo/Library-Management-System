from extensions import db
from datetime import date, timedelta


class Loan(db.Model):
    """
    Loan model for tracking book checkout transactions.

    Args:
        user_id (int): Foreign key reference to the borrowing user.
        book_copy_id (int): Foreign key reference to the borrowed book copy.
        loan_date (date, optional): Loan start date, defaults to today.
        return_date (date, optional): Expected return date, defaults to 14 days from today.
        is_returned (bool, optional): Return status, defaults to False.

    Attributes:
        id (int): Auto-generated primary key.
        user_id (int): Reference to the borrowing user.
        book_copy_id (int): Reference to the borrowed book copy.
        loan_date (date): Date when the book was loaned out.
        return_date (date): Expected return date (14-day default period).
        is_returned (bool): Whether the book has been returned.
        book_copy (relationship): Related BookCopy instance via backref.

    Returns:
        Loan: Loan model instance.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_copy_id = db.Column(db.Integer, db.ForeignKey('book_copy.id'), nullable=False)
    loan_date = db.Column(db.Date, nullable=False, default=date.today)
    return_date = db.Column(db.Date, nullable=False, default=lambda: date.today() + timedelta(days=14))
    is_returned = db.Column(db.Boolean, default=False)

    book_copy = db.relationship('BookCopy', backref='loans', lazy=True)

    def json(self):
        """
        Convert Loan object to JSON-serializable dictionary.

        Returns:
            dict: Dictionary containing loan id, user_id, book_copy_id, dates in ISO format, and return status.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_copy_id': self.book_copy_id,
            'loan_date': self.loan_date.isoformat(),
            'return_date': self.return_date.isoformat(),
            'is_returned': self.is_returned
        }
