from flask import Blueprint, request, jsonify
from services.book_copy_service import BookCopyService

book_copy_bp = Blueprint('book_copy', __name__)
book_copy_service = BookCopyService()


@book_copy_bp.route('', methods=['GET'])
def get_all_book_copies():
    """
    Get all book copies.

    Returns:
        200: List of all book copies.
    """
    copies = book_copy_service.get_all_copies()
    return jsonify([copy.json() for copy in copies]), 200


@book_copy_bp.route('/<int:book_copy_id>', methods=['GET'])
def get_book_copy(book_copy_id):
    """
    Get a specific book copy by ID.

    Args:
        book_copy_id (int): Book copy ID from URL path.

    Returns:
        200: Book copy details.
        404: Book copy not found.
    """
    copy = book_copy_service.get_copy_by_id(book_copy_id)
    return jsonify(copy.json()), 200


@book_copy_bp.route('', methods=['POST'])
def create_book_copy():
    """
    Create a new book copy.

    Args:
        JSON body: {'book_id': int, 'location': str, 'available': bool (optional)}

    Returns:
        201: Book copy created successfully.
        400: Missing required fields or validation error.
    """
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
    """
    Update an existing book copy.

    Args:
        book_copy_id (int): Book copy ID from URL path.
        JSON body: Fields to update (e.g., 'available', 'location').

    Returns:
        201: Book copy updated successfully.
        400: Missing data or validation error.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    copy, error = book_copy_service.update_copy(data, book_copy_id)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Book copy edited successfully',
        'book_copy': copy.json()}), 201


@book_copy_bp.route('/<int:book_copy_id>', methods=['DELETE'])
def delete_book_copy(book_copy_id):
    """
    Delete a book copy by ID.

    Args:
        book_copy_id (int): Book copy ID from URL path.

    Returns:
        204: Book copy deleted successfully.
        404: Book copy not found.
        400: Deletion error.
    """
    success, error = book_copy_service.delete_copy(book_copy_id)
    if error:
        if error == "Book copy not found":
            return jsonify({'error': error}), 404
        return jsonify({'error': error}), 400
    return '', 204


@book_copy_bp.route('/availability', methods=['GET'])
def get_available_book_copies():
    """
    List all available book copies with count per book.

    Returns:
        200: Available book copies grouped by book with counts.
    """
    copies = book_copy_service.get_available_copies_with_counts()
    return jsonify(copies), 200
