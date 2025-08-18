from extensions import db


class Book(db.Model):
    """
    Book model representing books in the library system.

    Args:
        title (str): Book title, max 150 characters.
        author_id (int): Foreign key reference to the author.
        category_id (int): Foreign key reference to the book category.

    Attributes:
        id (int): Auto-generated primary key.
        title (str): Book title, max 150 characters, required.
        author_id (int): Reference to the associated author.
        category_id (int): Reference to the book category.
        copies (relationship): One-to-many relationship with BookCopy instances.

    Returns:
        Book: Book model instance.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    copies = db.relationship('BookCopy', backref='book', lazy=True)

    def json(self):
        """
        Convert Book object to JSON-serializable dictionary.

        Returns:
            dict: Dictionary containing book id, title, author_id, and category_id.
        """
        return {
            'id': self.id,
            'title': self.title,
            'author_id': self.author_id,
            'category_id': self.category_id,
        }

