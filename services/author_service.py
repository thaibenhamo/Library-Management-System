
from models.author_model import Author
from repositories.author_repository import AuthorRepository


class AuthorService:
    """
    Service for Author-related business logic.

    Attributes:
        repo (AuthorRepository): Repository for Author persistence.
    """
    def __init__(self):
        """
        Initialize service with an AuthorRepository instance.
        """
        self.repo = AuthorRepository()

    def create_author(self, name):
        """
        Create and save a new author.

        Args:
            name (str): Author name.

        Returns:
            Author: Created Author instance.
        """
        author = Author(name=name)
        self.repo.save(author)
        self.repo.commit()
        return author

    def get_all_authors(self):
        """
        Return a list of all authors.

        Returns:
            list[Author]: All Author instances.
        """
        return self.repo.find_all()

    def get_author_by_id(self, author_id):
        """
        Get an author by their ID.

        Args:
            author_id (int): Author primary key.

        Returns:
            Author or None: Author instance if found, None otherwise.
        """
        return self.repo.find_by_id(author_id)

    def update_author(self, author_id, new_name):
        """
        Update the name of an existing author.

        Args:
            author_id (int): Author primary key.
            new_name (str): New author name.

        Returns:
            Author or None: Updated Author, or None if not found.
        """
        author = self.repo.find_by_id(author_id)
        if not author:
            return None
        author.name = new_name
        self.repo.commit()
        return author

    def delete_author(self, author_id):
        """
        Delete an author by ID.

        Args:
            author_id (int): Author primary key.

        Returns:
            bool: True if deleted, False if author not found.
        """
        author = self.repo.find_by_id(author_id)
        if not author:
            return False
        self.repo.delete(author)
        return True
