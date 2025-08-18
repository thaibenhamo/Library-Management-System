from models.book_copy_model import BookCopy
from repositories.book_copy_repository import BookCopyRepository
from services.book_service import BookService


class BookCopyService:
    """
    Service for business logic related to book copy management.

    Attributes:
        book_copy_repo (BookCopyRepository): Repository for book copy persistence.
        book_service (BookService): Service for book entity queries.
    """

    def __init__(self):
        """
        Initialize service with repositories.
        """
        self.book_copy_repo = BookCopyRepository()
        self.book_service = BookService()

    def get_all_copies(self):
        """
        Return all book copies.

        Returns:
            list[BookCopy]: All book copies.
        """
        return self.book_copy_repo.find_all()

    def get_copy_by_id(self, book_copy_id):
        """
        Return a book copy by ID.

        Args:
            book_copy_id (int): Book copy ID.

        Returns:
            BookCopy or None: Found book copy or None if not found.
        """
        return self.book_copy_repo.get_by_id(book_copy_id)

    def create_copy(self, book_id, available=True, location=None):
        """
        Create a new book copy for an existing book.

        Args:
            book_id (int): ID of the book to copy.
            available (bool, optional): Copy availability. Default True.
            location (str, optional): Location description.

        Returns:
            tuple[BookCopy | None, str | None]: (Created copy, None) or (None, error message)
        """
        if not isinstance(book_id, int):
            return None, "Book_id must be an integer"

        book = self.book_service.get_book_by_id(book_id)
        if not book:
            return None, "Book not found"

        book_copy = BookCopy(book_id=book_id, available=available, location=location)
        copy = self.book_copy_repo.save(book_copy)

        return (copy, None) if copy else (None, "Failed to create book copy")

    def update_copy(self, data, book_copy_id):
        """
        Update fields of an existing book copy.

        Args:
            data (dict): Fields to update ('book_id', 'available', 'location').
            book_copy_id (int): ID of copy to update.

        Returns:
            tuple[BookCopy | None, str | None]: (Updated copy, None) or (None, error message)
        """
        book_copy = self.book_copy_repo.get_by_id(book_copy_id)
        if not book_copy:
            return None, "Book copy not found"

        book_id = data.get('book_id')
        if book_id:
            if not isinstance(book_id, int):
                return None, "Book_id must be an integer"
            if not self.book_service.get_book_by_id(book_id):
                return None, "Book not found"
            book_copy.book_id = book_id

        if 'available' in data:
            available = data['available']
            if not isinstance(available, bool):
                return None, "Available must be a boolean"
            book_copy.available = available

        if 'location' in data:
            location = data['location']
            if not isinstance(location, str):
                return None, "Location must be a string"
            book_copy.location = location

        updated = self.book_copy_repo.update(book_copy)
        return (updated, None) if updated else (None, "Failed to edit book copy")

    def delete_copy(self, book_copy_id):
        """
        Delete a book copy by ID.

        Args:
            book_copy_id (int): Book copy ID.

        Returns:
            tuple[bool, str | None]: (True, None) if deleted, (False, error message) if not.
        """
        book_copy = self.book_copy_repo.get_by_id(book_copy_id)
        if not book_copy:
            return False, "Book copy not found"

        success = self.book_copy_repo.delete(book_copy_id)
        return (True, None) if success else (False, "Failed to delete book copy")

    def get_available_copies_with_counts(self):
        """
        Return all available copies and count per book.

        Returns:
            dict: {
                "available_copies": list of available copies (dicts),
                "count_per_book": {book_id: {"title": str, "count": int}, ...}
            }
        """
        available_copies = self.book_copy_repo.get_available_copies()
        book_counts = {}
        for copy in available_copies:
            book_id = copy.book_id
            if book_id not in book_counts:
                book_counts[book_id] = {
                    "title": copy.book.title if copy.book else "Unknown",
                    "count": 0
                }
            book_counts[book_id]["count"] += 1

        return {
            "available_copies": [copy.json() for copy in available_copies],
            "count_per_book": book_counts
        }
