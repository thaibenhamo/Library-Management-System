# routes/author_routes.py

from flask import Blueprint, request, jsonify
from services.author_service import AuthorService

author_bp = Blueprint('author_bp', __name__, url_prefix='/api/authors')
author_service = AuthorService()

@author_bp.route('', methods=['POST'])
def create_author():
    """
    Create a new author.
    Expects JSON with 'name' field.
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
    """
    authors = author_service.get_all_authors()
    return jsonify([author.json() for author in authors]), 200

@author_bp.route('/<int:author_id>', methods=['GET'])
def get_author(author_id):
    """
    Get an author by ID.
    """
    author = author_service.get_author_by_id(author_id)
    if not author:
        return jsonify({'error': 'Author not found'}), 404
    return jsonify(author.json()), 200

@author_bp.route('/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    """
    Update an author's name.
    Expects JSON with 'name' field.
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
    """
    success = author_service.delete_author(author_id)
    if not success:
        return jsonify({'error': 'Author not found'}), 404
    return jsonify({'message': 'Author deleted'}), 204
