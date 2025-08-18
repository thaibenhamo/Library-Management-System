
import requests
from models.book_model import Book
from models.author_model import Author
from models.category_model import Category
from repositories.author_repository import AuthorRepository
from repositories.category_repository import CategoryRepository
from repositories.book_repository import BookRepository
from extensions import db


class FillBooksService:
    """
    Service to fetch books from Google Books API and populate database.

    Attributes:
        author_repo (AuthorRepository): Repository for author persistence.
        category_repo (CategoryRepository): Repository for category persistence.
        book_repo (BookRepository): Repository for book persistence.
    """

    def __init__(self):
        """
        Initialize with repository instances.
        """
        self.author_repo = AuthorRepository()
        self.category_repo = CategoryRepository()
        self.book_repo = BookRepository()

    def fetch_and_store_books(self, query, limit):
        """
        Fetch books from the Google Books API using a search query and store them in the database.

        Parameters:
            query (str): The search query (e.g., "science fiction", "history").
            limit (int): The maximum number of books to fetch (max 40 per Google Books API docs).

        Returns:
            list[str]: Titles of books successfully added to the database.
        """
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={limit}"
        res = requests.get(url)
        items = res.json().get('items', [])
        created = []

        for item in items:
            info = item.get("volumeInfo", {})
            title = info.get("title")
            if not title:
                continue

            # Get first author/category or use defaults
            author_name = info.get("authors", ["Unknown Author"])[0]
            category_name = info.get("categories", ["General"])[0]

            # Find or create author
            author = self.author_repo.find_by_name(author_name)
            if not author:
                author = Author(name=author_name)
                self.author_repo.save(author)

            # Find or create category
            category = self.category_repo.find_by_name(category_name)
            if not category:
                category = Category(name=category_name)
                self.category_repo.save(category)

            # Skip if book with same title + author exists
            if self.book_repo.find_by_title_and_author(title, author.id):
                continue

            # Create and save new book
            book = Book(title=title, author_id=author.id, category_id=category.id)
            self.book_repo.save(book)
            created.append(title)

        db.session.commit()
        return created
