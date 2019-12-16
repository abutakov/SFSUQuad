#!/usr/bin/env python3

################################
#         forms.py             #
# basic form/validation logic  #
# Created by:                  #
# Emanuel Saunders(Nov 29,2019)#
################################

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User, Post
from app import photos

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
            raise ValidationError(f"An account already exists with given email: {email.data}")

class MessageForm(FlaskForm):
    body = TextAreaField( validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
    
class NewPostForm(FlaskForm):
    title = StringField("Post Title", validators=[DataRequired()])
    body = TextAreaField('Please describe your item', validators=[Length(min=1, max=140)])
    image = FileField(validators=[FileAllowed(photos, 'Please upload an image file (.jpg, .jpeg, .png)')])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search = StringField('Search for something new', validators=[Length(max=40)])