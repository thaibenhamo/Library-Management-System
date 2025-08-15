from flask import Blueprint, request, jsonify
from services.book_service import BookService
from services.fill_books_service import FillBooksService

import requests
from flask import request
from models.book_model import Book
from models.Author_model import Author
from models.category_model import Category
from extensions import db
from sqlalchemy.exc import SQLAlchemyError

book_bp = Blueprint('book_bp', __name__)
book_service = BookService()
fill_books_service = FillBooksService()

@book_bp.route('', methods=['POST'])
def add_book():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400

    if not data.get('author_id'):
        return jsonify({'error': 'Author ID is required'}), 400

    if not data.get('category_id'):
        return jsonify({'error': 'Category ID is required'}), 400

    book, error = book_service.create_book(
        title=data['title'],
        author_id=data['author_id'],
        category_id=data['category_id']
    )

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Book created successfully',
        'book': book.json()
    }), 201


@book_bp.route('', methods=['GET'])
def get_books():
    books = book_service.get_all_books()
    return jsonify([book.json() for book in books]), 200


@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = book_service.get_book_by_id(book_id)

    if not book:
        return jsonify({'error': 'Book not found'}), 404

    return jsonify(book.json()), 200


@book_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    success, message = book_service.delete_book(book_id)

    if not success:
        return jsonify({'error': message}), 404

    return jsonify({'message': message}), 204

@book_bp.route('/fill_external', methods=['POST'])
def fill_books():
    data = request.get_json()
    query = data.get('query', 'fiction')
    limit = min(int(data.get('limit', 10)), 40)

    try:
        created = fill_books_service.fetch_and_store_books(query, limit)
        return jsonify({
            "message": f"{len(created)} books added",
            "books": created
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
