from models.author_model import Author
from extensions import db


class AuthorRepository:
    """
    Repository class for handling database operations on Author entities.

    Provides CRUD operations and query methods for Author model instances,
    abstracting database access patterns and transaction management.

    Returns:
        AuthorRepository: Repository instance for Author operations.
    """

    def find_by_name(self, name):
        """
        Retrieve author by name from the database.

        Args:
            name (str): Author name to search for.

        Returns:
            Author or None: Author instance if found, None otherwise.
        """
        return db.session.query(Author).filter_by(name=name).first()

    def find_by_id(self, author_id):
        """
        Retrieve author by ID from the database.

        Args:
            author_id (int): Primary key ID of the author.

        Returns:
            Author or None: Author instance if found, None otherwise.
               """
        return db.session.get(Author, author_id)

    def find_all(self):
        """
        Retrieve all authors from the database.

        Returns:
            list[Author]: List of all Author instances.
        """
        return db.session.query(Author).all()

    def save(self, author):
        """
        Add new author to session and flush to database.

        Args:
            author (Author): Author instance to save.

        Returns:
            Author: The saved author instance with generated ID.
        """
        db.session.add(author)
        db.session.flush()
        return author

    def commit(self):
        """
        Commit current database transaction.

        Returns:
            None
        """
        db.session.commit()

    def delete(self, author):
        """
        Delete author from database and commit transaction.

        Args:
            author (Author): Author instance to delete.

        Returns:
            None
        """
        db.session.delete(author)
        db.session.commit()
