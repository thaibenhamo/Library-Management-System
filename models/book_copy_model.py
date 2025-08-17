from extensions import db


class BookCopy(db.Model):
    """
        BookCopy model representing individual physical copies of books.

        Args:
            book_id (int): Foreign key reference to the book.
            location (str): Physical shelf location of the copy.
            available (bool, optional): Availability status, defaults to True.

        Attributes:
            id (int): Auto-generated primary key.
            book_id (int): Reference to the associated book.
            available (bool): Whether the copy is available for checkout.
            location (str): Physical location/shelf identifier, max 100 characters.

        Returns:
            BookCopy: BookCopy model instance.
        """
    __tablename__ = 'book_copy'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    available = db.Column(db.Boolean, default=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)  # shelf location

    def json(self):
        """
            Convert BookCopy object to JSON-serializable dictionary.

            Args:
                None

            Returns:
                dict: Dictionary containing book copy id, book_id, availability status, and location.
        """
        return {
            'id': self.id,
            'book_id': self.book_id,
            'available': self.available,
            'location': self.location,
        }
