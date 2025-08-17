from extensions import db


class Category(db.Model):
    """
    Category model for organizing books by genre or classification.

    Args:
        name (str): Category name, max 50 characters.

    Attributes:
        id (int): Auto-generated primary key.
        name (str): Category name, max 50 characters, required.
        books (relationship): One-to-many relationship with Book instances.

    Returns:
        Category: Category model instance.
    """
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    books = db.relationship('Book', backref='category', lazy=True)

    def json(self):
        """
        Convert Category object to JSON-serializable dictionary.

        Returns:
            dict: Dictionary containing category id and name.
        """
        return {
            'id': self.id,
            'name': self.name
        }
