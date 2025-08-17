from extensions import db, bcrypt


def init_db(app):
    """
       Initialize database and hashing extensions for the Flask app, and create all tables.

       Args:
           app (Flask): Flask application instance.

       Returns:
           None
       """
    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        from models.user_model import User
        from models.category_model import Category
        from models.author_model import Author
        from models.book_model import Book
        from models.book_copy_model import BookCopy
        from models.loan_model import Loan
        db.create_all()

