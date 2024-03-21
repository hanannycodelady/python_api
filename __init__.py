from flask import Flask, request, jsonify
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token
import jwt
from authors_app.extensions import db, migrate, bcrypt
from authors_app.controllers.auth_controllers import auth
from authors_app.controllers.company_controllers import company
from authors_app.controllers.books_controllers import book
from authors_app.Models import users 

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Generate a secure random secret key
    secret_key = secrets.token_urlsafe(32)
    print("JWT Secret Key:", secret_key)

    # Configuring Flask-JWT-Extended with the generated secret key
    app.config['JWT_SECRET_KEY'] = secret_key
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'JWT'  
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = "X-CSRF-TOKEN"
    app.config['JWT_ACCESS_CSRF_FIELD_NAME'] = 'csrf_access_token'

    # Initializing SQLAlchemy and Flask-Migrate
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Register blueprints of the books,company and auth
    app.register_blueprint(auth)
    app.register_blueprint(book)
    app.register_blueprint(company)

    @app.route('/login', methods=['POST'])
    def login():
        # Get username and password from request
        username = request.json.get('username')
        password = request.json.get('password')


        if username == 'example_user' and password == 'password123':
            # If credentials are valid, generate JWT token
            access_token = create_access_token(identity=username)
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401

    @app.route('/protected', methods=['GET'])
    def protected():

        token = request.headers.get('Authorization')
        if token:
            token = token.split('Bearer ')[1]
        else:
            token = request.cookies.get('access_token')

        # Verify and decode token
        try:
            decoded_token = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            user_id = decoded_token['identity']
            return jsonify({'message': f'Protected resource accessed by user {user_id}'}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

    @app.route('/users', methods=['POST'])
    def create_user():
        # Extract user data from the request JSON
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Check if username and password are provided
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        # Check if the username is already taken
        existing_user = users.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400

        # Create a new user object
        new_user = users(username=username, password=password)

        # Add the new user to the database session
        db.session.add(new_user)
        
        try:
            # Commit the changes to the database
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            # Rollback the transaction in case of any error
            db.session.rollback()
            return jsonify({'error': 'Failed to create user', 'details': str(e)}), 500

    @app.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        # Extract user data from the request JSON
        data = request.json
        new_username = data.get('username')
        new_password = data.get('password')

        # Retrieve the user from the database
        user = user.query.get(user_id)

        # Check if the user exists
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Update the user's username if provided
        if new_username:
            # Check if the new username is already taken
            existing_user = user.query.filter_by(username=new_username).first()
            if existing_user and existing_user.id != user_id:
                return jsonify({'error': 'Username already exists'}), 400
            user.username = new_username

        # Update the user's password if provided
        if new_password:
            user.password = new_password

        # Commit the changes to the database
        try:
            db.session.commit()
            return jsonify({'message': 'User updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update user', 'details': str(e)}), 500

    @app.route('/')
    def home():
        return "Hello programmers"
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
















