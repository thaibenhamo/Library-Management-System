from flask import Blueprint, request, jsonify
from services.book_service import BookService

book_bp = Blueprint('book_bp', __name__)
book_service = BookService()

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