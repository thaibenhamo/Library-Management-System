from flask import Blueprint, request, jsonify
from services.category_service import CategoryService

category_bp = Blueprint('category_bp', __name__)
category_service = CategoryService()

@category_bp.route('', methods=['POST'])
def add_category():
    """
    Create a new category.
    Expects JSON with 'name' field.
    """
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Category name is required'}), 400

    category, error = category_service.create_category(data['name'])
    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Category created',
        'category': category.json()
    }), 201

@category_bp.route('', methods=['GET'])
def get_all_categories():
    """
    Get a list of all categories.
    """
    categories = category_service.get_all_categories()
    return jsonify([category.json() for category in categories]), 200

@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    """
    Get category details by ID.
    """
    category = category_service.get_category_by_id(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify(category.json()), 200

@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """
    Delete a category by ID.
    """
    success, error = category_service.delete_category(category_id)
    if not success:
        return jsonify({'error': error}), 404
    return jsonify({'message': 'Category deleted'}), 204

@category_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """
    Update a category's name.
    Expects JSON with 'name' field.
    """
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400

    updated_category, error = category_service.update_category(category_id, data['name'])
    if error:
        return jsonify({'error': error}), 400

    return jsonify(updated_category.json()), 200
