from flask import Blueprint, request, jsonify
from authors_app.Models.book import Book
from authors_app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import JWTManager

book = Blueprint('book', __name__, url_prefix='/api/v1/book')

@book.route('/register', methods=['POST'])
def register_books():
    try:
        
        title = request.json.get('title')# Extracting request data
        description = request.json.get('description')
        price = request.json.get('price')
        price_unit = request.json.get('price_unit')
        pages = request.json.get('pages')
        publication_date = request.json.get('publication_date')
        isbn = request.json.get('isbn')
        genre = request.json.get('genre')
        user_id = request.json.get('user_id')

     

        # Basic input validation
        if not all([title, description, price, price_unit, pages, publication_date, isbn, genre, user_id]):
            return jsonify({"error": 'All fields are required'}), 400

        
        # Creating a new book
        new_book = Book(
            title=title,
            description=description,
            price=float(price),
            price_unit=price_unit,
            pages=int(pages),
            publication_date=publication_date,
            isbn=isbn,
            genre=genre,
            user_id=int(user_id),
        
        )

        #  committing to the database
        db.session.add(new_book)
        db.session.commit()

        # Building a response message
        return jsonify({"message": f"Book '{new_book.title}', ID '{new_book.id}' has been uploaded"}), 201

    except Exception as e:
        
        return jsonify({"error": str(e)}), 500
    
    

@book.route("/<int:id>") 
@jwt_required()
def get_book(id):
    try:
        current_user = get_jwt_identity()  
        book = Book.query.filter_by(user_id=current_user, id=id).first()

        if not book:
            return jsonify({'error': 'Item not found'}), 404
        
        # Return book details
        return jsonify({
            'id': book.id,
            'title': book.title,
            'description': book.description,
            'price': book.price,
            'price_unit': book.price_unit,
            'pages': book.pages,
            'publication_date': book.publication_date,
            'isbn': book.isbn,
            'genre': book.genre,
            'user_id': book.user_id
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500






    
    
    
        
    