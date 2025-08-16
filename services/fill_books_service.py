import requests
from models.book_model import Book
from models.Author_model import Author
from models.category_model import Category
from repositories.author_repository import AuthorRepository
from repositories.category_repository import CategoryRepository
from repositories.book_repository import BookRepository
from extensions import db

class FillBooksService:
    def __init__(self):
        self.author_repo = AuthorRepository()
        self.category_repo = CategoryRepository()
        self.book_repo = BookRepository()

    def fetch_and_store_books(self, query, limit):
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={limit}"
        res = requests.get(url)
        items = res.json().get('items', [])
        created = []

        for item in items:
            info = item.get("volumeInfo", {})
            title = info.get("title")

            if not title:
                continue

            author_name = info.get("authors", ["Unknown Author"])[0]
            category_name = info.get("categories", ["General"])[0]

            author = self.author_repo.find_by_name(author_name)
            if not author:
                author = Author(name=author_name)
                self.author_repo.save(author)

            category = self.category_repo.find_by_name(category_name)
            if not category:
                category = Category(name=category_name)
                self.category_repo.save(category)

            if self.book_repo.find_by_title_and_author(title, author.id):
                continue

            book = Book(title=title, author_id=author.id, category_id=category.id)
            self.book_repo.save_for_api(book)
            created.append(title)

        db.session.commit()
        return created
