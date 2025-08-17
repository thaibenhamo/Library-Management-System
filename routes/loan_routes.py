from flask import Blueprint, request, jsonify
from services.loan_service import LoanService

loan_bp = Blueprint('loan_bp', __name__)
loan_service = LoanService()


@loan_bp.route('', methods=['GET'])
def get_all_loans():
    """
    Get all loans for current user.

    Args:
        Query parameter: user_id (int)

    Returns:
        200: List of user's loans.
        400: Missing user_id parameter.
    """
    current_user_id = request.args.get('user_id', type=int)
    if not current_user_id:
        return jsonify({'error': 'Missing user_id in query parameters'}), 400

    loans = loan_service.get_loans_by_user(current_user_id)
    return jsonify({'loans': loans}), 200


@loan_bp.route('', methods=['POST'])
def create_loan():
    """
    Create a new loan.

    Args:
        JSON body: {'user_id': int, 'book_copy_id': int}

    Returns:
        201: Loan created successfully.
        400: Missing required fields or book already on loan.
        500: Server error.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing JSON body'}), 400

        current_user_id = data.get('user_id')
        book_copy_id = data.get('book_copy_id')

        if not current_user_id:
            return jsonify({'error': 'Missing user_id'}), 400
        if not book_copy_id:
            return jsonify({'error': 'Missing book_copy_id'}), 400

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
    """
    Return a borrowed book.

    Args:
        loan_id (int): Loan ID from URL path.
        JSON body: {'user_id': int}

    Returns:
        200: Book returned successfully.
        400: Missing user_id or return error.
    """
    data = request.get_json()

    if not data or 'user_id' not in data:
        return jsonify({'error': 'Missing user_id in request body'}), 400

    user_id = data['user_id']
    loan, error = loan_service.return_loan(loan_id, user_id)

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Book returned successfully',
        'loan': loan
    }), 200


@loan_bp.route('/<int:loan_id>', methods=['GET'])
def get_loan_by_id(loan_id):
    """
    Get a specific loan by ID for current user.

    Args:
        loan_id (int): Loan ID from URL path.
        Query parameter: user_id (int)

    Returns:
        200: Loan details.
        400: Missing user_id parameter.
        404: Loan not found.
    """
    current_user_id = request.args.get('user_id', type=int)
    if not current_user_id:
        return jsonify({'error': 'Missing user_id in query parameters'}), 400

    loan, error = loan_service.get_loan_by_id_for_user(loan_id, current_user_id)
    if error:
        return jsonify({'error': error}), 404
    return jsonify({'loan': loan}), 200


@loan_bp.route('/stats', methods=['GET'])
def loan_statistics():
    """
    Get loan statistics (total, returned, not returned counts).

    Returns:
        200: Loan statistics summary.
    """
    stats = loan_service.get_loan_statistics()
    return jsonify(stats), 200


@loan_bp.route('/user/<int:user_id>', methods=['GET'])
def get_loans_by_user_id(user_id):
    """
    Get loan history for a specific user.

    Args:
        user_id (int): User ID from URL path.

    Returns:
        200: List of user's loans.
    """
    loans = loan_service.get_loans_by_user(user_id)
    return jsonify({'loans': loans}), 200
