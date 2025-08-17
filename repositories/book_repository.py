from models.book_model import Book
from extensions import db
from sqlalchemy import func

class BookRepository:
    def __init__(self, db_session=None):
        self.db_session = db_session or db.session

    def find_all(self):
        """Get all books"""
        try:
            stmt = db.select(Book)
            return self.db_session.scalars(stmt).all()
        except Exception as e:
            print(f"Error getting all books: {e}")
            return []

    def get_by_id(self, book_id):
        """Get book by ID"""
        try:
            return self.db_session.get(Book, book_id)
        except Exception as e:
            print(f"Error getting book by ID {book_id}: {e}")
            return None

    def get_by_title(self, title):
        """Get book by title"""
        try:
            return self.db_session.query(Book).filter(Book.title == title).first()
        except Exception as e:
            print(f"Error getting book by title {title}: {e}")
            return None

    def find_by_title_and_author(self, title, author_id):
        return self.db_session.query(Book).filter_by(title=title, author_id=author_id).first()

    def save(self, book):
        try:
            self.db_session.add(book)
            self.db_session.commit()
            return book, None

        except Exception as e:
            self.db_session.rollback()
            return None, f"Error creating book: {e}"

    def save_for_api(self, book):
        try:
            self.db_session.add(book)
            return book, None
        except Exception as e:
            self.db_session.rollback()
            return None, f"Error creating book: {e}"

    def delete(self, book_id):
        """Delete a book by ID"""
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
        """Update an existing book"""
        try:
            self.db_session.commit()
            return book
        except Exception as e:
            self.db_session.rollback()
            print(f"Error updating book {book.id}: {e}")
            return None

    def commit(self):
        db.session.commit()

    def find_by_title(self, title):
        title = title.strip()
        return db.session.query(Book).filter(func.lower(Book.title) == func.lower(title)).first()



