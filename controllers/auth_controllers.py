from flask import Blueprint, request, jsonify
from authors_app.Models.users import User, db
from flask_bcrypt import Bcrypt
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import jwt_required, get_jwt_identity


auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
bcrypt = Bcrypt()

#Defining the registration endpoints of the api
@auth.route('/register', methods=['POST'])
def register():
    try:
        
        first_name = request.json.get('first_name')# Extracting request data
        last_name = request.json.get('last_name')
        contact = request.json.get('contact')
        email = request.json.get('email')
        user_type = request.json.get('user_type', 'author')  # Default to 'author'
        password = request.json.get('password')
        biography = request.json.get('biography', '') if user_type == 'author' else ''

        # Basic validation inputs
        required_fields = ['first_name', 'last_name', 'contact', 'password', 'email']
        if not all(request.json.get(field) for field in required_fields):
            return jsonify({'error': 'All fields are required'}), 400

        if user_type == 'author' and not biography:
            return jsonify({'error': 'Enter your author biography'}), 400

        #Password validation
        if len(password) < 6:
           return jsonify({'error': 'Password is too short'}), 400

        # Email validation
        try:
            validate_email(email)
        except EmailNotValidError:
            return jsonify({'error': 'Email is not valid'}), 400
# validating email and cotact
        if User.query.filter_by(email=email).first() is not None:
            return jsonify({'error': 'Email already exists'}), 409

        if User.query.filter_by(contact=contact).first() is not None:
            return jsonify({'error': 'Contact already exists'}), 409

        #Creating a new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(first_name=first_name, last_name=last_name, email=email,
                        contact=contact, password=hashed_password, user_type=user_type,
                        biography=biography)

        #Adding data to the database
        db.session.add(new_user)
        db.session.commit()

        # costructing a response
        username = f"{new_user.first_name} {new_user.last_name}"
        return jsonify({
            'message': f'{username} has been successfully created as an {new_user.user_type}',
            'user': {
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'contact': new_user.contact,
                'type': new_user.user_type,
                'biography': new_user.biography,
                'created_at': new_user.created_at,
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@auth.route("/<int:id>") 
@jwt_required()
def get_book(id):
    try:
        current_user = get_jwt_identity()  # Get current user using get_jwt_identity
        book = User.query.filter_by(user_id=current_user, id=id).first()

        if not book:
            return jsonify({'error': 'Item not found'}), 404
        
        # Return book details
        return jsonify({
            'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                'email': current_user.email,
                'contact': current_user.contact,
                'type': current_user.user_type,
                'biography': current_user.biography,
                'created_at': current_user.created_at,
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#defining a login endpoint
@auth.route('/login', methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        #retrieving the user by email
        User = User.query.filter_by(email=email).first()
        # Check if the user exists and the password is correct
        if User and bcrypt.check_password_hash(User.password, password):
            # Return a response that is successful
            return jsonify({'message': 'Login successful', 'user_id': User.id}), 200
        else:
            # Return an error response if authentication fails
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Defining the edit user endpoint
@auth.route('/edit/<int:user_id>', methods=["PUT"])
def edit_user(user_id):
    try:
        # Extract user data from the request json
        data = request.json
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Updating user's fields if given in the request
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            # Check if the new email already exists
            new_email = data['email']
            if new_email != user.email and User.query.filter_by(email=new_email).first():
                return jsonify({'error': 'The email already exists'}), 400
            user.email = new_email
        if 'image' in data:
            user.image = data['image']
        if 'biography' in data:
            user.biography = data['biography']
        if 'user_type' in data:
            user.user_type = data['user_type']
        if 'password' in data:
            password = data['password']
            if len(password) < 6:
                return jsonify({'error': 'Password must have at least 6 characters'}), 400
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        if 'contact' in data:
            user.contact = data['contact']

        # Commit the session to save the changes in the database
        db.session.commit()

        # Return  response that is successfull
        return jsonify({'message': 'User updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500    
    
## Definining the delete user endpoint
@auth.route('/delete/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
#pushes  the user's data to the database
        db.session.commit()
    

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 
    
    
@auth.route('/users', methods=["GET"])
def get_all_users():
    try:
        users = User.query.all()

        # Serialize user's data
        serialized_users = []
        for user in users:
            serialized_user = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'image': user.image,
                'biography': user.biography,
                'user_type': user.user_type,
                'contact': user.contact
            }
            serialized_users.append(serialized_user)

        # Return the serialized user's data
        return jsonify({'users': serialized_users}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@auth.route('/user/<int:user_id>', methods=["GET"])

def get_user(user_id):
        try:
            user = User.query.get(user_id)

            # Check if the user exists
            if user:
                serialized_user = {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'image': user.image,
                    'biography': user.biography,
                    'user_type': user.user_type,
                    'contact': user.contact
                }
                # Return the serialized user data
                return jsonify({'user': serialized_user}), 200
            else:
                return jsonify({'error': 'User not found'}), 404

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
