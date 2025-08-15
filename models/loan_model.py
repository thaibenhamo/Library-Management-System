from extensions import db
from datetime import date, timedelta


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_copy_id = db.Column(db.Integer, db.ForeignKey('book_copy.id'), nullable=False)
    loan_date = db.Column(db.Date, nullable=False, default=date.today)
    return_date = db.Column(db.Date, nullable=False, default=lambda: date.today() + timedelta(days=14))
    is_returned = db.Column(db.Boolean, default=False)

    book_copy = db.relationship('BookCopy', backref='loans', lazy=True)

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_copy_id': self.book_copy_id,
            'loan_date': self.loan_date.isoformat(),
            'return_date': self.return_date.isoformat(),
            'is_returned': self.is_returned
        }
