from app import db, login
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from datetime import datetime


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'<User | {self.username}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True, default="")
    last_name = db.Column(db.String(30), nullable=False, unique=True)
    phone = db.Column(db.String(17), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, last_name, phone,user_id):
        self.name = name
        self.last_name = last_name
        self.phone = phone
        self.user_id = user_id

    def __repr__(self):
        return f'<Post | {self.title}>'



# ----------------------------------------------------------------------------------------------------


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description= db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image= db.Column(db.String(30), nullable=False)


    def __init__(self,  name, description,price,category, image):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.image = image

    def __repr__(self):
        return f'<Post | {self.name}>'



class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    description= db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image= db.Column(db.String(30), nullable=False)

    def __init__(self,  name, description,price,category,image):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.image = image

    def __repr__(self):
        return f'<Post | {self.name}>'    

    
    @classmethod
    def gettotal(cls):
        produc = ShoppingCart.query.all()
        total=0
        for prod in produc:
            total+=prod.price 
        return total     