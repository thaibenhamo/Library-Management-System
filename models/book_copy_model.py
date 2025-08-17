from extensions import db


class BookCopy(db.Model):
    __tablename__ = 'book_copy'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    available = db.Column(db.Boolean, default=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)  # shelf location

    def json(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'available': self.available,
            'location': self.location,
        }
