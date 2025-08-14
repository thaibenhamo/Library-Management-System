from models.book_model import Book
from config.database import db
from sqlalchemy.exc import IntegrityError
from models.Author_model import Author

class BookService:
    def get_all_books(self):
        return Book.query.all()

    def get_book_by_id(self, book_id):
        return Book.query.get(book_id)

    def create_book(self, title, author_id, category_id):
        # Check author exists
        if not Author.query.get(author_id):
            return None, "Author ID does not exist"

        # Optional: Check category exists if needed
        # from models.category_model import Category
        # if not Category.query.get(category_id):
        #     return None, "Category ID does not exist"

        book = Book(title=title, author_id=author_id, category_id=category_id)
        db.session.add(book)

        try:
            db.session.commit()
            return book, None
        except IntegrityError:
            db.session.rollback()
            return None, "Integrity error occurred"

    def delete_book(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return False, "Book not found"

        db.session.delete(book)
        db.session.commit()
        return True, "Book deleted"