from flask import Blueprint, request, jsonify
from authors_app.Models.company import Company, db
from authors_app.Models.users import User

company = Blueprint('company', __name__, url_prefix='/api/v1/company')

@company.route('/register', methods=['POST'])
def register_company():
    try:
        # Extracting request data
        name = request.json.get('name')
        origin = request.json.get('origin')
        description = request.json.get('description')
        user_id = request.json.get('user_id')  

        # Basic input validation

        if not name:
            return jsonify({"error": 'Company name is required'}), 400

        if not origin:
            return jsonify({"error": 'Company origin is required'}), 400

        if not description:
            return jsonify({"error": 'Company description is required'}), 400

        # Check if the user already exists
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": 'User with the provided ID does not exist'}), 404

        # Creating a new company
        new_company = Company(
            name=name,
            origin=origin,
            description=description,
            user_id=user_id
        )

        db.session.add(new_company)
        db.session.commit()

        # Building a response message
        message = f"Company '{new_company.name}' with ID '{new_company.id}' has been registered"
        return jsonify({"message": message}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
