from models.category_model import Category
from repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def create_category(self, name):
        existing = self.repo.find_by_name(name)
        if existing:
            return None, "Category already exists"

        category = Category(name=name)
        self.repo.save(category)
        self.repo.commit()
        return category, None

    def get_all_categories(self):
        return self.repo.find_all()

    def get_category_by_id(self, category_id):
        return self.repo.find_by_id(category_id)

    def delete_category(self, category_id):
        category = self.repo.find_by_id(category_id)
        if not category:
            return False, "Category not found"
        self.repo.delete(category)
        return True, None

    def update_category(self, category_id, new_name):
        category = self.repo.find_by_id(category_id)
        if not category:
            return None, "Category not found"

        category.name = new_name

        try:
            self.repo.save(category)
            return category, None
        except Exception as e:
            return None, str(e)

