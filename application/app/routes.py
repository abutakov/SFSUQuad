#!/usr/bin/env python3

################################
#         routes.py            #
# Main website routing/control #
# Created by:                  #
# Emanuel Saunders(Nov 20,2019)#
################################

from flask import render_template, flash, redirect, url_for, request, send_from_directory    
from app import app, db, photos
from app.forms import LoginForm, RegistrationForm, NewPostForm, MessageForm
from app.models import User, Post, Message
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from werkzeug import secure_filename
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        query = request.form["search"]
        search = f'%{query}%'
        posts = Post.query.filter(Post.title.like(search)).all()
        return render_template('search.html', query=query, posts=posts)
    return render_template('index.html')

# Checks if user is logged in and returns to original page. 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Incorrect Password or Username')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        user.hash_user()
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    form = NewPostForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            filename = secure_filename(form.image.data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.image.data.save(file_path)
            print(f'filename: {filename}\nfile_path: {file_path}')
            post = Post(title=form.title.data, body=form.body.data, user_email=current_user.email, image=filename)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been made! Please wait at least 24 hours for it to go live.')
            return redirect(url_for('index'))
        else: 
            return redirect("login")
    return render_template("create_post.html", title="Create Post", form=form)


@login_required
@app.route('/user/<hash_id>')
def user(hash_id):
    user = User.query.filter_by(hash_id=hash_id).first_or_404()
    posts = Post.query.filter_by(user_email=user.email)
    num_posts = 0
    for post in posts:
        num_posts += 1
    return render_template('user.html', user=user, posts=posts, num_posts=num_posts)

@app.route('/post/<post_id>/')
def view_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('post.html', post=post)

@app.route('/uploads/<filename>')
def send_file(filename):
    print("\n getting file...")
    print(app.config['UPLOAD_FOLDER'])
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@login_required
@app.route('/post/<id>/send_message/', methods=['GET', 'POST'])
def send_message(id):
    form = MessageForm()
    post = Post.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        message = Message(post=id, sender=current_user.id, body=form.body.data )
        db.session.add(message)
        db.session.commit()
        flash('Message has been sent to sender!')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('view_post', post_id=id)
        return redirect(next_page)
    return render_template('send_message.html', id=id, form=form, post=post)