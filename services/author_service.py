# services/author_service.py
from models.Author_model import Author
from config.database import db

class AuthorService:
    def create_author(self, name):
        author = Author(name=name)
        db.session.add(author)
        db.session.commit()
        return author

    def get_all_authors(self):
        return Author.query.all()

    def get_author_by_id(self, author_id):
        return Author.query.get(author_id)

    def update_author(self, author_id, new_name):
        author = Author.query.get(author_id)
        if not author:
            return None
        author.name = new_name
        db.session.commit()
        return author

    def delete_author(self, author_id):
        author = Author.query.get(author_id)
        if not author:
            return False
        db.session.delete(author)
        db.session.commit()
        return True
