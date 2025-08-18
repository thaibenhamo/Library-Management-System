from models.book_model import Book
from extensions import db
from sqlalchemy import func


class BookRepository:
    """
    Repository class for managing Book database operations with comprehensive error handling.

    Provides CRUD operations, query methods, and specialized operations for Book model instances,
    including case-insensitive searches and API-specific methods.

    Args:
        db_session (Session, optional): Database session instance, defaults to db.session.

    Attributes:
        db_session (Session): Database session for executing queries.

    Returns:
        BookRepository: Repository instance for Book operations.
    """
    def __init__(self, db_session=None):
        """
        Initialize repository with database session.

        Args:
            db_session (Session, optional): Custom database session, defaults to db.session.
        """
        self.db_session = db_session or db.session

    def find_all(self):
        """
        Retrieve all books from the database with error handling.

        Returns:
            list[Book]: List of all Book instances, empty list on error.
        """
        try:
            stmt = db.select(Book)
            return self.db_session.scalars(stmt).all()
        except Exception as e:
            print(f"Error getting all books: {e}")
            return []

    def get_by_id(self, book_id):
        """
        Retrieve book by ID with error handling.

        Args:
            book_id (int): Primary key ID of the book.

        Returns:
            Book or None: Book instance if found, None on error or not found.
        """
        try:
            return self.db_session.get(Book, book_id)
        except Exception as e:
            print(f"Error getting book by ID {book_id}: {e}")
            return None

    def get_by_title(self, title):
        """
        Retrieve book by exact title match with error handling.

        Args:
            title (str): Exact title of the book to search.

        Returns:
            Book or None: First book matching title, None on error or not found.
        """
        try:
            return self.db_session.query(Book).filter(Book.title == title).first()
        except Exception as e:
            print(f"Error getting book by title {title}: {e}")
            return None

    def find_by_title_and_author(self, title, author_id):
        """
        Retrieve book by title and author combination.

        Args:
            title (str): Book title to search.
            author_id (int): Author ID to match.

        Returns:
            Book or None: Book matching both criteria, None if not found.
        """
        return self.db_session.query(Book).filter_by(title=title, author_id=author_id).first()

    def save(self, book):
        """
        Save new book to database with transaction management and commit.

        Args:
            book (Book): Book instance to save.

        Returns:
            tuple: (Book, None) on success or (None, error_message) on failure.
        """
        try:
            self.db_session.add(book)
            self.db_session.commit()
            return book, None

        except Exception as e:
            self.db_session.rollback()
            return None, f"Error creating book: {e}"

    def delete(self, book_id):
        """
        Delete book by ID with transaction management.

        Args:
            book_id (int): Primary key ID of book to delete.

        Returns:
            bool: True if successfully deleted, False otherwise.
        """
        try:
            book = self.get_by_id(book_id)
            if book:
                self.db_session.delete(book)
                self.db_session.commit()
                return True
            return False
        except Exception as e:
            self.db_session.rollback()
            print(f"Error deleting book {book_id}: {e}")
            return False

    def update(self, book):
        """
        Commit changes to existing book with rollback on error.

        Args:
            book (Book): Modified Book instance to update.

        Returns:
            Book or None: Updated book on success, None on failure.
        """
        try:
            self.db_session.commit()
            return book
        except Exception as e:
            self.db_session.rollback()
            print(f"Error updating book {book.id}: {e}")
            return None

    def commit(self):
        """
        Commit current database transaction.

        Returns:
            None
        """
        db.session.commit()

    def find_by_title(self, title):
        """
        Case-insensitive book search by title with whitespace trimming.

        Args:
            title (str): Book title to search (case-insensitive).

        Returns:
            Book or None: First book matching title (case-insensitive), None if not found.
        """
        title = title.strip()
        return db.session.query(Book).filter(func.lower(Book.title) == func.lower(title)).first()



