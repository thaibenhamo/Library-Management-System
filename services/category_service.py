
from models.category_model import Category
from repositories.category_repository import CategoryRepository


class CategoryService:
    """
    Service for business logic and validation related to categories.

    Attributes:
        repo (CategoryRepository): Repository for category persistence.
    """
    def __init__(self):
        """
        Initialize service with CategoryRepository.
        """
        self.repo = CategoryRepository()

    def create_category(self, name):
        """
        Create a new category.

        Returns an error if a category with the same name already exists.

        Args:
            name (str): Category name.

        Returns:
            tuple[Category | None, str | None]: (Created category, None) or (None, error message)
        """
        existing = self.repo.find_by_name(name)
        if existing:
            return None, "Category already exists"

        category = Category(name=name)
        self.repo.save(category)
        self.repo.commit()
        return category, None

    def get_all_categories(self):
        """
        Return a list of all categories.

        Returns:
            list[Category]: All categories.
        """
        return self.repo.find_all()

    def get_category_by_id(self, category_id):
        """
        Return a category by its ID.

        Args:
            category_id (int): Category primary key.

        Returns:
            Category or None: Found category or None.
        """
        return self.repo.find_by_id(category_id)

    def delete_category(self, category_id):
        """
        Delete a category by ID.

        Returns an error if the category is not found.

        Args:
            category_id (int): Category primary key.

        Returns:
            tuple[bool, str | None]: (True, None) if deleted, (False, error message) if not.
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

        Args:
            category_id (int): Category primary key.
            new_name (str): New name for the category.

        Returns:
            tuple[Category | None, str | None]: (Updated category, None) or (None, error message)
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
