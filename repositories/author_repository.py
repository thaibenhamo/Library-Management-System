from models.Author_model import Author
from extensions import db

class AuthorRepository:
    def find_by_name(self, name):
        return db.session.query(Author).filter_by(name=name).first()

    def save(self, author):
        db.session.add(author)
        db.session.flush()
        return author
