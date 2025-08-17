from models.author_model import Author
from extensions import db

class AuthorRepository:
    """
    Handles database operations for Author entities.
    """

    def find_by_name(self, name):
        """Get author by name."""
        return db.session.query(Author).filter_by(name=name).first()

    def find_by_id(self, author_id):
        """Get author by ID."""
        return db.session.get(Author, author_id)

    def find_all(self):
        """Get all authors."""
        return db.session.query(Author).all()

    def save(self, author):
        """Add and flush a new author."""
        db.session.add(author)
        db.session.flush()
        return author

    def commit(self):
        """Commit current transaction."""
        db.session.commit()

    def delete(self, author):
        """Delete author and commit."""
        db.session.delete(author)
        db.session.commit()
