"""
Service layer for managing book-related operations.
Coordinates validation and cross-entity checks for authors and categories.
"""

from models.book_model import Book
from repositories.book_repository import BookRepository
from services.author_service import AuthorService
from services.category_service import CategoryService


class BookService:
    """
    Service for business logic and validation related to books.

    Attributes:
        book_repo (BookRepository): Persistence for books.
        author_service (AuthorService): For author lookups/validation.
        category_service (CategoryService): For category lookups/validation.
    """

    def __init__(self):
        """
        Initialize service with dependencies.
        """
        self.book_repo = BookRepository()
        self.author_service = AuthorService()
        self.category_service = CategoryService()

    def get_all_books(self):
        """
        Return a list of all books.

        Returns:
            list[Book]: All books.
        """
        return self.book_repo.find_all()

    def get_book_by_id(self, book_id):
        """
        Return a single book by its ID.

        Args:
            book_id (int): Primary key.

        Returns:
            Book or None: Found book or None.
        """
        return self.book_repo.get_by_id(book_id)

    def create_book(self, title, author_id, category_id):
        """
        Create a new book.

        Validates title, author and category existence, and uniqueness by title.

        Args:
            title (str): Book title.
            author_id (int): Linked author ID.
            category_id (int): Linked category ID.

        Returns:
            tuple[Book | None, str | None]: (Created book, None) or (None, error message)
        """
        if not isinstance(title, str) or not title.strip():
            return None, "Title must be a non-empty string"

        if not isinstance(author_id, int):
            return None, "Author_id must be an integer"

        if not isinstance(category_id, int):
            return None, "Category_id must be an integer"

        if self.book_repo.get_by_title(title.strip()):
            return None, "Book with this title already exists"

        if not self.author_service.get_author_by_id(author_id):
            return None, "Author not found"

        if not self.category_service.get_category_by_id(category_id):
            return None, "Category not found"

        book = Book(title=title.strip(), author_id=author_id, category_id=category_id)
        saved_book, save_error = self.book_repo.save(book)
        return (saved_book, None) if saved_book else (None, save_error)

    def update_book(self, book_id, data):
        """
        Update book details (title, author, category).

        Validates all inputs and ensures title uniqueness.

        Args:
            book_id (int): Book primary key.
            data (dict): Fields to update.

        Returns:
            tuple[Book | None, str | None]: (Updated book, None) or (None, error message)
        """
        book = self.book_repo.get_by_id(book_id)
        if not book:
            return None, "Book not found"

        title = data.get('title')
        if title is not None:
            if not isinstance(title, str) or not title.strip():
                return None, "Title must be a non-empty string"

            existing = self.book_repo.get_by_title(title.strip())
            if existing and existing.id != book_id:
                return None, "Book with this title already exists"

            book.title = title.strip()

        author_id = data.get('author_id')
        if author_id is not None:
            if not isinstance(author_id, int):
                return None, "Author_id must be an integer"
            if not self.author_service.get_author_by_id(author_id):
                return None, "Author not found"
            book.author_id = author_id

        category_id = data.get('category_id')
        if category_id is not None:
            if not isinstance(category_id, int):
                return None, "Category_id must be an integer"
            if not self.category_service.get_category_by_id(category_id):
                return None, "Category not found"
            book.category_id = category_id

        updated = self.book_repo.update(book)
        return (updated, None) if updated else (None, "Failed to update book")

    def delete_book(self, book_id):
        """
        Delete a book by ID.

        Prevents deletion if book has existing copies.

        Args:
            book_id (int): Book primary key.

        Returns:
            tuple[bool, str | None]: (True, None) if deleted, (False, error) if not.
        """
        book = self.book_repo.get_by_id(book_id)
        if not book:
            return False, "Book not found"

        if book.copies and len(book.copies) > 0:
            return False, "Cannot delete book with existing copies"

        success = self.book_repo.delete(book_id)
        return (True, None) if success else (False, "Failed to delete book")

    def get_book_by_title(self, title):
        """
        Return a book by its title.

        Args:
            title (str): Book title.

        Returns:
            Book or None: Book if found, None otherwise.
        """
        return self.book_repo.find_by_title(title)
