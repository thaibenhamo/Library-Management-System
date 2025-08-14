from flask import Blueprint, request, jsonify
from services.loan_service import LoanService

loan_bp = Blueprint('loan_bp', __name__)
loan_service = LoanService()


@loan_bp.route('', methods=['GET'])
def get_all_loans():
    """Get all loans"""
    loans = loan_service.get_all_loans()
    return jsonify({'loans': loans}), 200


# Not tested yet
@loan_bp.route('', methods=['POST'])
def create_loan():
    """Create a new loan"""
    try:
        data = request.get_json()

        required_fields = ['user_id', 'book_copy_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

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


