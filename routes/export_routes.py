# routes/export_routes.py
from flask import Blueprint, send_file
from extensions import db
from models.book_model import Book
from models.Author_model import Author
from models.category_model import Category
from models.book_copy_model import BookCopy  # adjust name if different
from models.loan_model import Loan
from models.user_model import User
from utils.export_utils import rows_to_dataframe, make_xlsx_bytes

export_bp = Blueprint("export_bp", __name__, url_prefix="/api/export")

def _as_xlsx_response(sheets: dict[str, "pd.DataFrame"], filename: str):
    xlsx_io = make_xlsx_bytes(sheets)
    return send_file(
        xlsx_io,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=filename,
        max_age=0,
    )

@export_bp.route("/books.xlsx", methods=["GET"])
def export_books():
    rows = db.session.query(Book).all()
    return _as_xlsx_response({"books": rows_to_dataframe(rows)}, "books.xlsx")

@export_bp.route("/authors.xlsx", methods=["GET"])
def export_authors():
    rows = db.session.query(Author).all()
    return _as_xlsx_response({"authors": rows_to_dataframe(rows)}, "authors.xlsx")

@export_bp.route("/categories.xlsx", methods=["GET"])
def export_categories():
    rows = db.session.query(Category).all()
    return _as_xlsx_response({"categories": rows_to_dataframe(rows)}, "categories.xlsx")

@export_bp.route("/book_copies.xlsx", methods=["GET"])
def export_book_copies():
    rows = db.session.query(BookCopy).all()
    return _as_xlsx_response({"book_copies": rows_to_dataframe(rows)}, "book_copies.xlsx")

@export_bp.route("/loans.xlsx", methods=["GET"])
def export_loans():
    rows = db.session.query(Loan).all()
    return _as_xlsx_response({"loans": rows_to_dataframe(rows)}, "loans.xlsx")

@export_bp.route("/users.xlsx", methods=["GET"])
def export_users():
    rows = db.session.query(User).all()
    return _as_xlsx_response({"users": rows_to_dataframe(rows)}, "users.xlsx")

@export_bp.route("/all.xlsx", methods=["GET"])
def export_all():
    sheets = {
        "books":       rows_to_dataframe(db.session.query(Book).all()),
        "authors":     rows_to_dataframe(db.session.query(Author).all()),
        "categories":  rows_to_dataframe(db.session.query(Category).all()),
        "book_copies": rows_to_dataframe(db.session.query(BookCopy).all()),
        "loans":       rows_to_dataframe(db.session.query(Loan).all()),
        "users":       rows_to_dataframe(db.session.query(User).all()),
    }
    return _as_xlsx_response(sheets, "library_export.xlsx")
