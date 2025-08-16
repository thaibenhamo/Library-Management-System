from models.category_model import Category
from extensions import db

class CategoryRepository:
    def find_by_name(self, name):
        return db.session.query(Category).filter_by(name=name).first()

    def find_by_id(self, category_id):
        return db.session.get(Category, category_id)

    def find_all(self):
        return db.session.query(Category).all()

    def save(self, category):
        db.session.add(category)
        db.session.flush()
        return category

    def commit(self):
        db.session.commit()

    def delete(self, category):
        db.session.delete(category)
        db.session.commit()

