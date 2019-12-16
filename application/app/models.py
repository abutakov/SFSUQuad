
################################
#         models.py            #
# Database object definitions  #
# Created by:                  #
# Emanuel Saunders(Nov 25,2019)#
################################

from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
# Handles required fields for user model class
from flask_login import UserMixin
from hashlib import md5

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='User', lazy='dynamic')
    messages = db.relationship('Message', backref='User', lazy='dynamic')
    username = db.Column(db.String(128), index=True, unique=True)

    def set_username(self):
        temp = self.email.lower()
        index = temp.find("@")
        self.username = temp[0:index]
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# defines how to print out class items
    def __repr__(self):
        return f'[User:{self.username}]'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), index=True)
    body = db.Column(db.String(240))
    image = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_email = db.Column(db.String(128), db.ForeignKey('user.email'))
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'[Post:{self.title}, timestamp:{self.timestamp}, \
                  owner:{self.User.hash_id} active:{self.active}]'
    

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, db.ForeignKey('post.id'))
    sender = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(40))    

    def __repr__(self):
        return f'[From:{self.sender} To: {self.post.owner_id}, Msg: {self.content}]'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer)

    def __repr__(self):
        return f'[Id:{self.id}, Name: {self.name}]'
