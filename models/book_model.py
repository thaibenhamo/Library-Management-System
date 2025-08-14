from extensions import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    copies = db.relationship('BookCopy', backref='book', lazy=True)

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'author_id': self.author_id,
            'category_id': self.category_id,
            'quantity': self.quantity
        }