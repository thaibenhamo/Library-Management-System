from models.category_model import Category
from extensions import db

class CategoryRepository:
    def find_by_name(self, name):
        return db.session.query(Category).filter_by(name=name).first()

    def save(self, category):
        db.session.add(category)
        db.session.flush()
        return category
