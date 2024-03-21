from authors_app.extensions import db
#from app.extentions import db,bcrypt
from datetime import datetime
from authors_app.extensions import db, migrate


class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)#all datatypes start with capital letter eg Integer,String
    first_name=db.Column(db.String(50),nullable=False)
    last_name=db.Column(db.String(100),nullable=False)
    image=db.Column(db.String(255),nullable=True)
    email=db.Column(db.String(100),nullable=False,unique=True)
    contact=db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.Text(),nullable=False)
    biography=db.Column(db.Text(),nullable=True)
   # book=db.relationship('Book',bacref='users')
    user_type=db.Column(db.String(20),default='author')
    created_at=db.Column(db.DateTime,default=datetime.now())
    updated_at=db.Column(db.DateTime,onupdate=datetime.now())

    def __init__(self,first_name,last_name,email,contact,password,biography,user_type,image=None):
        self.first_name=first_name
        self.last_name=last_name
        self.email=email
        self.user_type=user_type
        self.contact=contact
        self.image=image
        self.biography=biography
        self.password=password






























# from authors_app.extensions import db
# from datetime import datetime
# from authors_app.extensions import db, migrate


# class User(db.Model): # The model must be a captial letter
#     __tablename__ = 'Users'
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(100))
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     contact = db.Column(db.Integer, primary_key=True, unique=True)
#     # image = db.Column(db.String(255), nullable=True)
#     # usertype = db.Column(db.String(100), nullable=True)
#     created_at = db.Column(db.DateTime, default=datetime.now())
#     update_at = db.Column(db.DateTime, onupdate=datetime.now())
#     password = db.Column(db.String(100), nullable=False, unique=True)
    
    
#     def __init__(self,first_name,last_name,biography,user_type,password,email,contact,image=None):
#         self.first_name=first_name
#         self.last_name=last_name
#         self.email= email
#         self.contact= contact
#         self.image= image
#         self.biography=biography
#         self.password=password
#         self.user_type=user_type

#     def get_full_name(self):
#         return f'{self.last_name} {self.first_name}'
