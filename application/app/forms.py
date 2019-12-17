#!/usr/bin/env python3

################################
#         forms.py             #
# basic form/validation logic  #
# Created by:                  #
# Emanuel Saunders(Nov 29,2019)#
################################

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User, Post, Category
from app import photos, db
#forms used for users, includes validation

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Please enter SFSU email")])
    password = PasswordField('Password', validators=[DataRequired()])  
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email(message="Please enter SFSU email")])

    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Create Account')

    # checks if email already in database
    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("An account already exists with given email: {}".format(email.data))

class MessageForm(FlaskForm):
    body = TextAreaField( validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
    
def get_categories():
    return Category.query

class NewPostForm(FlaskForm):
    title = StringField("Post Title", validators=[DataRequired()])
    body = TextAreaField('Post Details', validators=[Length(min=1, max=140)])
    price = FloatField('Item Price')
    category = QuerySelectField('Select a Category',
    query_factory = get_categories,
    allow_blank = False) 
    image = FileField("Upload an Image", validators=[FileAllowed(photos, 'Please upload an image file (.jpg, .jpeg, .png)')])
    submit = SubmitField('Submit')
