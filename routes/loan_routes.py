from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.loan_service import LoanService

loan_bp = Blueprint('loan_bp', __name__)
loan_service = LoanService()

@loan_bp.route('', methods=['GET'])
def get_all_loans():
    """Get all loans for current user"""
    current_user_id = get_jwt_identity()
    loans = loan_service.get_loans_by_user(current_user_id)
    return jsonify({'loans': loans}), 200


@loan_bp.route('', methods=['POST'])
def create_loan():
    """Create a new loan"""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()

        if not data.get('book_copy_id'):
            return jsonify({'error': 'Missing required field: book_copy_id'}), 400

        data['user_id'] = current_user_id
        loan, error = loan_service.create_loan(data)

        if error:
            if error == "Book is already on loan":
                return jsonify({'error': error}), 400
            return jsonify({'error': error}), 500

        return jsonify({
            'message': 'Loan created successfully',
            'loan': loan
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@loan_bp.route('/<int:loan_id>/return', methods=['PUT'])
def return_book(loan_id):
    current_user_id = get_jwt_identity()
    loan, error = loan_service.return_loan(loan_id, current_user_id)

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Book returned successfully',
        'loan': loan
    }), 200


@loan_bp.route('/<int:loan_id>', methods=['GET'])
def get_loan_by_id(loan_id):
    current_user_id = get_jwt_identity()
    loan, error = loan_service.get_loan_by_id_for_user(loan_id, current_user_id)
    if error:
        return jsonify({'error': error}), 404
    return jsonify({'loan': loan}), 200
