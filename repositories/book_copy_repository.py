from extensions import db
from models.book_copy_model import BookCopy


class BookCopyRepository:
    def __init__(self, db_session=None):
        self.db_session = db_session or db.session

    def find_all(self):
        """Get all book copies"""
        try:
            stmt = db.select(BookCopy)
            return self.db_session.scalars(stmt).all()
        except Exception as e:
            raise

    def get_by_id(self, book_copy_id):
        """Get book copy by ID"""
        try:
            return self.db_session.get(BookCopy, book_copy_id)
        except Exception as e:
            print(f"Error getting book copy by ID {book_copy_id}: {e}")

    def save(self, book_copy):
        """Create a new book copy"""
        try:
            self.db_session.add(book_copy)
            self.db_session.commit()
            return book_copy
        except Exception as e:
            self.db_session.rollback()
            return None, f"Error creating book copy: {e}"

    def update(self, book_copy):
        """Update an existing book copy"""
        try:
            self.db_session.commit()
            return book_copy
        except Exception as e:
            self.db_session.rollback()
            print(f"Error updating book copy {book_copy.id}: {e}")

    # TODO: implement DELETE method

