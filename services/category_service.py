from models.category_model import Category
from extensions import db

class CategoryService:
    def create_category(self, name):
        existing = Category.query.filter_by(name=name).first()
        if existing:
            return None, "Category already exists"

        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category, None

    def get_all_categories(self):
        return Category.query.all()

    def get_category_by_id(self, category_id):
        return Category.query.get(category_id)

    def delete_category(self, category_id):
        category = self.get_category_by_id(category_id)
        if not category:
            return False, "Category not found"
        db.session.delete(category)
        db.session.commit()
        return True, None
