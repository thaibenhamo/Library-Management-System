from extensions import db
from models.book_copy_model import BookCopy


class BookCopyRepository:
    """
    Repository class for managing BookCopy database operations with error handling.

    Provides CRUD operations and query methods for BookCopy model instances,
    including transaction management and exception handling.

    Args:
        db_session (Session, optional): Database session instance, defaults to db.session.

    Attributes:
        db_session (Session): Database session for executing queries.

    Returns:
        BookCopyRepository: Repository instance for BookCopy operations.
    """

    def __init__(self, db_session=None):
        """
        Initialize repository with database session.

        Args:
            db_session (Session, optional): Custom database session, defaults to db.session.

        Returns:
            None
        """
        self.db_session = db_session or db.session

    def find_all(self):
        """
        Retrieve all book copies from the database.

        Returns:
            list[BookCopy]: List of all BookCopy instances.

        Raises:
            Exception: Re-raises any database exceptions encountered.
        """
        try:
            stmt = db.select(BookCopy)
            return self.db_session.scalars(stmt).all()
        except Exception as e:
            raise

    def get_by_id(self, book_copy_id):
        """
        Retrieve book copy by ID with error handling.

        Args:
            book_copy_id (int): Primary key ID of the book copy.

        Returns:
            BookCopy or None: BookCopy instance if found, None if error occurs.
        """
        try:
            return self.db_session.get(BookCopy, book_copy_id)
        except Exception as e:
            print(f"Error getting book copy by ID {book_copy_id}: {e}")

    def save(self, book_copy):
        """
        Save new book copy to database with transaction management.

        Args:
            book_copy (BookCopy): BookCopy instance to save.

        Returns:
            tuple: (BookCopy, None) on success or (None, error_message) on failure.
        """
        try:
            self.db_session.add(book_copy)
            self.db_session.commit()
            return book_copy
        except Exception as e:
            self.db_session.rollback()
            return None, f"Error creating book copy: {e}"

    def update(self, book_copy):
        """
        Commit changes to existing book copy with rollback on error.

        Args:
            book_copy (BookCopy): Modified BookCopy instance to update.

        Returns:
            BookCopy or None: Updated book copy on success, None on failure.
        """
        try:
            self.db_session.commit()
            return book_copy
        except Exception as e:
            self.db_session.rollback()
            print(f"Error updating book copy {book_copy.id}: {e}")

    def delete(self, book_copy_id):
        """
        Delete book copy by ID with transaction management.

        Args:
            book_copy_id (int): Primary key ID of book copy to delete.

        Returns:
            bool: True if successfully deleted, False otherwise.
        """
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
        """
        Retrieve all currently available book copies.

        Returns:
            list[BookCopy]: List of BookCopy instances where available=True.
        """
        return self.db_session.query(BookCopy).filter_by(available=True).all()
