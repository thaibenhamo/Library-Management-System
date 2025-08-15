from models.book_model import Book
from repositories.book_repository import BookRepository
from services.author_service import AuthorService
from services.category_service import CategoryService


class BookService:
    def __init__(self):
        self.book_repo = BookRepository()
        self.author_service = AuthorService()
        self.category_service = CategoryService()

    def get_all_books(self):
        """Get all books"""
        return self.book_repo.find_all()

    def get_book_by_id(self, book_id):
        """Get book by ID"""
        return self.book_repo.get_by_id(book_id)

    def create_book(self, title, author_id, category_id):
        if not isinstance(title, str) or not title.strip():
            return None, "Title must be a non-empty string"

        if not isinstance(author_id, int):
            return None, "Author_id must be an integer"

        if not isinstance(category_id, int):
            return None, "Category_id must be an integer"

        existing_book = self.book_repo.get_by_title(title.strip())
        if existing_book:
            return None, "Book with this title already exists"

        if not self.author_service.get_author_by_id(author_id):
            return None, "Author not found"
        if not self.category_service.get_category_by_id(category_id):
            return None, "Category not found"

        book = Book(title=title.strip(), author_id=author_id, category_id=category_id)

        saved_book, save_error = self.book_repo.save(book)
        if save_error:
            return None, save_error

        return saved_book, None

    def update_book(self, book_id, data):
        """Update a book"""
        book = self.book_repo.get_by_id(book_id)
        if not book:
            return None, "Book not found"

        title = data.get('title')
        if title is not None:
            if not isinstance(title, str) or not title.strip():
                return None, "Title must be a non-empty string"

            # Check if new title already exists (excluding current book)
            existing_book = self.book_repo.get_by_title(title.strip())
            if existing_book and existing_book.id != book_id:
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

        updated_book = self.book_repo.update(book)
        if updated_book:
            return updated_book, None
        return None, "Failed to update book"

    def delete_book(self, book_id):
        """Delete a book"""
        book = self.book_repo.get_by_id(book_id)
        if not book:
            return False, "Book not found"

        if book.copies and len(book.copies) > 0:
            return False, "Cannot delete book with existing copies"

        success = self.book_repo.delete(book_id)
        if success:
            return True, None
        return False, "Failed to delete book"

