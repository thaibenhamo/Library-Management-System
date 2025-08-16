# services/author_service.py
from models.Author_model import Author
from config.database import db

from models.Author_model import Author
from repositories.author_repository import AuthorRepository

class AuthorService:
    def __init__(self):
        self.repo = AuthorRepository()

    def create_author(self, name):
        author = Author(name=name)
        self.repo.save(author)
        self.repo.commit()
        return author

    def get_all_authors(self):
        return self.repo.find_all()

    def get_author_by_id(self, author_id):
        return self.repo.find_by_id(author_id)

    def update_author(self, author_id, new_name):
        author = self.repo.find_by_id(author_id)
        if not author:
            return None
        author.name = new_name
        self.repo.commit()
        return author

    def delete_author(self, author_id):
        author = self.repo.find_by_id(author_id)
        if not author:
            return False
        self.repo.delete(author)
        return True

