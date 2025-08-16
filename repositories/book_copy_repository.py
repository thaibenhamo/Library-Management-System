from extensions import db
from models.book_copy_model import BookCopy

class BookCopyRepository:
    """
    Repository class for managing BookCopy database operations.
    """

    def __init__(self, db_session=None):
        self.db_session = db_session or db.session

    def find_all(self):
        """Return all book copies."""
        try:
            stmt = db.select(BookCopy)
            return self.db_session.scalars(stmt).all()
        except Exception as e:
            raise

    def get_by_id(self, book_copy_id):
        """Return a book copy by ID."""
        try:
            return self.db_session.get(BookCopy, book_copy_id)
        except Exception as e:
            print(f"Error getting book copy by ID {book_copy_id}: {e}")

    def save(self, book_copy):
        """Save a new book copy to the database."""
        try:
            self.db_session.add(book_copy)
            self.db_session.commit()
            return book_copy
        except Exception as e:
            self.db_session.rollback()
            return None, f"Error creating book copy: {e}"

    def update(self, book_copy):
        """Commit changes to an existing book copy."""
        try:
            self.db_session.commit()
            return book_copy
        except Exception as e:
            self.db_session.rollback()
            print(f"Error updating book copy {book_copy.id}: {e}")

    def delete(self, book_copy_id):
        """Delete a book copy by ID."""
        try:
            book_copy = self.db_session.get(BookCopy, book_copy_id)
            if book_copy:
                self.db_session.delete(book_copy)
                self.db_session.commit()
                return True
            return False
        except Exception as e:
            self.db_session.rollback()
            print(f"Error deleting book copy {book_copy_id}: {e}")
            return False

    def get_available_copies(self):
        """Return all currently available book copies."""
        return self.db_session.query(BookCopy).filter_by(available=True).all()
