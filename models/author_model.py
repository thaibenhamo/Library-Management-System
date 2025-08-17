from extensions import db


class Author(db.Model):
    """
    Author model representing authors in the system.

    Args:
        name (str): Author's display name.

    Attributes:
        id (int): Auto-generated primary key.
        name (str): Author name with 100 character limit.

    Returns:
        Author: Author model instance.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def json(self):
        """
        Serialize Author instance to dictionary format.

        Returns:
            dict: Author data as dictionary with 'id' and 'name' keys.
        """
        return {
            'id': self.id,
            'name': self.name
        }
