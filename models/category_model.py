from extensions import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }
