
from flask import Blueprint, request, jsonify
from services.book_copy_service import BookCopyService

book_copy_bp = Blueprint('book_copy', __name__)

book_copy_service = BookCopyService()


@book_copy_bp.route('', methods=['GET'])
def get_all_book_copies():
    """Get all book copies"""
    copies = book_copy_service.get_all_copies()

    return jsonify([copy.to_dict() for copy in copies]), 200


# Not tested yet
@book_copy_bp.route('/<int:book_copy_id>', methods=['GET'])
def get_book_copy(book_copy_id):
    """Get a specific book copy by ID"""
    copy = book_copy_service.get_copy_by_id(book_copy_id)
    if copy:
        return jsonify(copy.to_dict()), 200


@book_copy_bp.route('', methods=['POST'])
def create_book_copy():
    """Create a new book copy"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    if not data.get('book_id'):
        return jsonify({'error': 'book_id is required'}), 400

    if not data.get('location'):
        return jsonify({'error': 'location is required'}), 400

    book_id = data['book_id']
    available = data.get('available', True)
    location = data.get('location')

    copy, error = book_copy_service.create_copy(book_id, available, location)

    if error:
        return jsonify({'error': error}), 400
    return jsonify({
        'message': 'Book copy created successfully',
        'book_copy': copy.json()}), 201


@book_copy_bp.route('/<int:book_copy_id>', methods=['PUT'])
def update_book_copy(book_copy_id):
    """Update an existing book copy"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    copy, error = book_copy_service.update_copy(data, book_copy_id)

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Book copy edited successfully',
        'book_copy': copy.json()}), 201

