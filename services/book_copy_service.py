# services/book_copy_service.py
from models.book_copy_model import BookCopy
from repositories.book_copy_repository import BookCopyRepository
from services.book_service import BookService


class BookCopyService:
    def __init__(self):
        self.book_copy_repo = BookCopyRepository()
        self.book_service = BookService()

    def get_all_copies(self):
        """Get all book copies with book details"""
        return self.book_copy_repo.find_all()

    def get_copy_by_id(self, book_copy_id):
        """Get book copy by ID with book details"""
        return self.book_copy_repo.get_by_id(book_copy_id)

    def create_copy(self, book_id, available=True, location=None):
        """Create a new book copy"""
        if not isinstance(book_id, int):
            return None, "Book_id must be an integer"

        book = self.book_service.get_book_by_id(book_id)

        if not book:
            return None, "Book not found"

        book_copy = BookCopy(
            book_id=book_id,
            available=available,
            location=location
        )

        copy = self.book_copy_repo.save(book_copy)

        if copy:
            return copy, None
        return None, "Failed to create book copy"

    def update_copy(self, data, book_copy_id):
        """Update a book copy"""
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

        available = data.get('available')
        if available is not None:
            if not isinstance(available, bool):
                return None, "Available must be a boolean"
            book_copy.available = available

        location = data.get('location')
        if location:
            if not isinstance(location, str):
                return None, "Location must be a string"
            book_copy.location = location

        copy = self.book_copy_repo.update(book_copy)
        if copy:
            return copy, None
        return None, "Failed to edit book copy"

    def delete_copy(self, book_copy_id):
        """Delete a book copy"""
        book_copy = self.book_copy_repo.get_by_id(book_copy_id)
        if not book_copy:
            return False, "Book copy not found"

        success = self.book_copy_repo.delete(book_copy_id)
        if success:
            return True, None
        return False, "Failed to delete book copy"
