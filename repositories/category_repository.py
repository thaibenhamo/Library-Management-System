from models.category_model import Category
from extensions import db


class CategoryRepository:
    """
    Repository class for managing Category-related database operations.

    Provides CRUD operations and query methods for Category model instances,
    abstracting database access patterns and transaction management.

    Returns:
        CategoryRepository: Repository instance for Category operations.
    """

    def find_by_name(self, name):
        """
        Retrieve category by name from the database.

        Args:
            name (str): Category name to search for.

        Returns:
            Category or None: Category instance if found, None otherwise.
        """
        return db.session.query(Category).filter_by(name=name).first()

    def find_by_id(self, category_id):
        """
        Retrieve category by ID from the database.

        Args:
            category_id (int): Primary key ID of the category.

        Returns:
            Category or None: Category instance if found, None otherwise.
        """
        return db.session.get(Category, category_id)

    def find_all(self):
        """
        Retrieve all categories from the database.

        Returns:
            list[Category]: List of all Category instances.
        """
        return db.session.query(Category).all()

    def save(self, category):
        """
        Add new category to session and flush to database.

        Args:
            category (Category): Category instance to save.

        Returns:
            Category: The saved category instance with generated ID.
        """
        db.session.add(category)
        db.session.flush()
        return category

    def commit(self):
        """
        Commit current database transaction.

        Returns:
            None
        """
        db.session.commit()

    def delete(self, category):
        """
        Delete category from database and commit transaction.

        Args:
            category (Category): Category instance to delete.

        Returns:
            None
        """
        db.session.delete(category)
        db.session.commit()
