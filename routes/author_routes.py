from flask import Blueprint, request, jsonify
from services.author_service import AuthorService

author_bp = Blueprint('author_bp', __name__, url_prefix='/api/authors')
author_service = AuthorService()


@author_bp.route('', methods=['POST'])
def create_author():
    """
    Create a new author.

    Args:
        JSON body: {'name': str}

    Returns:
        201: Author created successfully.
        400: Missing author name.
    """
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Author name is required'}), 400

    author = author_service.create_author(data['name'])
    return jsonify({'message': 'Author created', 'author': author.json()}), 201


@author_bp.route('', methods=['GET'])
def get_authors():
    """
    Get a list of all authors.

    Returns:
        200: List of all authors.
    """
    authors = author_service.get_all_authors()
    return jsonify([author.json() for author in authors]), 200


@author_bp.route('/<int:author_id>', methods=['GET'])
def get_author(author_id):
    """
    Get an author by ID.

    Args:
        author_id (int): Author ID from URL path.

    Returns:
        200: Author details.
        404: Author not found.
    """
    author = author_service.get_author_by_id(author_id)
    if not author:
        return jsonify({'error': 'Author not found'}), 404
    return jsonify(author.json()), 200


@author_bp.route('/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    """
    Update an author's name.

    Args:
        author_id (int): Author ID from URL path.
        JSON body: {'name': str}

    Returns:
        200: Author updated successfully.
        400: Missing name field.
        404: Author not found.
    """
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400

    author = author_service.update_author(author_id, data['name'])
    if not author:
        return jsonify({'error': 'Author not found'}), 404

    return jsonify({'message': 'Author updated', 'author': author.json()}), 200


@author_bp.route('/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    """
    Delete an author by ID.

    Args:
        author_id (int): Author ID from URL path.

    Returns:
        204: Author deleted successfully.
        404: Author not found.
    """
    success = author_service.delete_author(author_id)
    if not success:
        return jsonify({'error': 'Author not found'}), 404
    return jsonify({'message': 'Author deleted'}), 204
