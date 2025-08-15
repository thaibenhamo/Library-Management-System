from models.book_model import Book
from extensions import db

class BookRepository:
    def find_by_title_and_author(self, title, author_id):
        return db.session.query(Book).filter_by(title=title, author_id=author_id).first()

    def save(self, book):
        db.session.add(book)
        return book
