from models.Author_model import Author
from extensions import db

class AuthorRepository:
    def find_by_name(self, name):
        return db.session.query(Author).filter_by(name=name).first()

    def find_by_id(self, author_id):
        return db.session.get(Author, author_id)

    def find_all(self):
        return db.session.query(Author).all()

    def save(self, author):
        db.session.add(author)
        db.session.flush()
        return author

    def commit(self):
        db.session.commit()

    def delete(self, author):
        db.session.delete(author)
        db.session.commit()

