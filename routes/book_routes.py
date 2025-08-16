from flask import Blueprint, request, jsonify
from services.book_service import BookService
from services.fill_books_service import FillBooksService


from flask import request
from extensions import db

book_bp = Blueprint('book_bp', __name__)
book_service = BookService()
fill_books_service = FillBooksService()


@book_bp.route('', methods=['GET'])
def get_books():
    """Get all books"""
    books = book_service.get_all_books()
    return jsonify([book.json() for book in books]), 200


@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book by ID"""
    book = book_service.get_book_by_id(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book.json()), 200


@book_bp.route('', methods=['POST'])
def add_book():
    """Create a new book"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        required_fields = ['title', 'author_id', 'category_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

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

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@book_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update an existing book"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        book, error = book_service.update_book(book_id, data)
        if error:
            if error == "Book not found":
                return jsonify({'error': error}), 404
            return jsonify({'error': error}), 400

        return jsonify({
            'message': 'Book updated successfully',
            'book': book.json()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@book_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book by ID"""
    success, error = book_service.delete_book(book_id)

    if error:
        if error == "Book not found":
            return jsonify({'error': error}), 404
        return jsonify({'error': error}), 400

    return '', 204


@book_bp.route('/fill_external', methods=['POST'])
def fill_books():
    data = request.get_json()
    query = data.get('query', 'fiction')
    limit = min(int(data.get('limit', 10)), 40)

    try:
        created = fill_books_service.fetch_and_store_books(query, limit)
        print(f"FillBooksService called with query='{query}' and limit={limit}")

        return jsonify({
            "message": f"{len(created)} books added",
            "books": created
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@book_bp.route('/by-title/<string:title>', methods=['GET'])
def get_book_by_title(title):
    """Get a book by its title"""
    book = book_service.get_book_by_title(title)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book.json()), 200

