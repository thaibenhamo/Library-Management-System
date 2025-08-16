"""
Service layer for managing categories.
Handles creation, retrieval, update, and deletion of category records.
"""

from models.category_model import Category
from repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def create_category(self, name):
        """
        Create a new category.
        Returns error if category with the same name already exists.
        """
        existing = self.repo.find_by_name(name)
        if existing:
            return None, "Category already exists"

        category = Category(name=name)
        self.repo.save(category)
        self.repo.commit()
        return category, None

    def get_all_categories(self):
        """Return a list of all categories."""
        return self.repo.find_all()

    def get_category_by_id(self, category_id):
        """Return a category by its ID."""
        return self.repo.find_by_id(category_id)

    def delete_category(self, category_id):
        """
        Delete a category by ID.
        Returns an error if the category is not found.
        """
        category = self.repo.find_by_id(category_id)
        if not category:
            return False, "Category not found"
        self.repo.delete(category)
        return True, None

    def update_category(self, category_id, new_name):
        """
        Update a category's name.
        Returns error if category is not found or save fails.
        """
        category = self.repo.find_by_id(category_id)
        if not category:
            return None, "Category not found"

        category.name = new_name

        try:
            self.repo.save(category)
            return category, None
        except Exception as e:
            return None, str(e)
