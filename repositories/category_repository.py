from models.category_model import Category
from extensions import db

class CategoryRepository:
    """
    Repository class for managing Category-related database operations.
    """

    def find_by_name(self, name):
        """Return the category with the given name, or None if not found."""
        return db.session.query(Category).filter_by(name=name).first()

    def find_by_id(self, category_id):
        """Return the category with the given ID, or None if not found."""
        return db.session.get(Category, category_id)

    def find_all(self):
        """Return all categories."""
        return db.session.query(Category).all()

    def save(self, category):
        """Add a new category to the session and flush it."""
        db.session.add(category)
        db.session.flush()
        return category

    def commit(self):
        """Commit the current session."""
        db.session.commit()

    def delete(self, category):
        """Delete a category and commit the change."""
        db.session.delete(category)
        db.session.commit()
