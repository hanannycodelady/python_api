from authors_app import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    pages = db.Column(db.Integer)
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    publication_date = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String(30), nullable=True, unique=True)
    genre = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, title, description, pages, price, price_unit, publication_date, isbn, genre, user_id):
        self.title = title
        self.description = description
        self.pages = pages
        # self.image = image
        self.price = price
        self.price_unit = price_unit
        self.publication_date = publication_date
        self.isbn = isbn
        self.genre = genre
        self.user_id = user_id

    def __repr__(self):
        return f'<Book {self.title}>'














# from authors_app import db
# from datetime import datetime



# class Book(db.Model):
#     __tablename__='books'
#     id=db.Column(db.Integer,primary_key=True)#all datatypes start with capital letter eg Integer,String
#     title=db.Column(db.String(50),nullable=False)
#     price=db.Column(db.String(100),nullable=False)
#     pages=db.Column(db.Integer)
#     description=db.Column(db.String(100))
#     user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
#     company_id=db.Column(db.Integer,db.ForeignKey('companies.id'))
#     publication_date=db.Column(db.Date,nullable=False)
#     isbn = db.Column(db.String(30), nullable=True, unique=True)
#     genre = db.Column(db.String(50), nullable=False)

#     #user=db.relationship('user',backref='books')
#     #company=db.relationship('company',backref='books')
#     created_at=db.Column(db.DateTime,default=datetime.now())
#     updated_at=db.Column(db.DateTime,onupdate=datetime.now())

#     # creating an instance
#     def __init__(self,title,description,pages,image,price,price_unit,publication_date,isbn,genre,user_id,):
#         self.title=title
#         self.description=description
#         self.price = price
#         self.price_unit = price_unit
#         self.pages = pages
#         self.publication_date = publication_date
#         self.isbn = isbn
#         self.genre = genre
#         self.user_id = user_id
#         self.image = image

#         self.user_id=user_id
#         self.pages=pages
#     def __init__(self):
#         return f'<Book{self.title}'



























# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from authors_app.extensions import db
# from datetime import datetime
# from authors_app.extensions import db



# class Book (db.Model):
#     __tablename__ = "books"
#     id =  db.Column(db.Integer, primary_key= True)
#     title = db.Column(db.String(100), nullable=False)
#     pages = db.Column(db.Integer,nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#     description = db.Column(db.String(100))
#     image = db.Column(db.String(255))
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
#     created_at = db.Column(db.DateTime, default=datetime.now())
#     updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    
#     def __init__(self, title, description, pages, users_id, price, user_id, image=None):
#         self.users_id = users_id
#         self.pages = pages
#         self.title = title
#         self.description = description
#         self.users_id = users_id
#         self.price = price
#         self.image = image
