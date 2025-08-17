"""
Service layer for managing book copy operations.
Handles creation, updates, deletions, and availability checks for book copies.
"""

from models.book_copy_model import BookCopy
from repositories.book_copy_repository import BookCopyRepository
from services.book_service import BookService


class BookCopyService:
    def __init__(self):
        self.book_copy_repo = BookCopyRepository()
        self.book_service = BookService()

    def get_all_copies(self):
        """Return all book copies."""
        return self.book_copy_repo.find_all()

    def get_copy_by_id(self, book_copy_id):
        """Return a book copy by ID."""
        return self.book_copy_repo.get_by_id(book_copy_id)

    def create_copy(self, book_id, available=True, location=None):
        """Create a new book copy for an existing book."""
        if not isinstance(book_id, int):
            return None, "Book_id must be an integer"

        book = self.book_service.get_book_by_id(book_id)
        if not book:
            return None, "Book not found"

        book_copy = BookCopy(book_id=book_id, available=available, location=location)
        copy = self.book_copy_repo.save(book_copy)

        return (copy, None) if copy else (None, "Failed to create book copy")

    def update_copy(self, data, book_copy_id):
        """Update fields of an existing book copy."""
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
        """Delete a book copy by ID."""
        book_copy = self.book_copy_repo.get_by_id(book_copy_id)
        if not book_copy:
            return False, "Book copy not found"

        success = self.book_copy_repo.delete(book_copy_id)
        return (True, None) if success else (False, "Failed to delete book copy")

    def get_available_copies_with_counts(self):
        """Return all available copies and count per book."""
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
