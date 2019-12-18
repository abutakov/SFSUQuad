#!/usr/bin/env python3

################################
#         routes.py            #
# Main website routing/control #
# Created by:                  #
# Emanuel Saunders(Nov 20,2019)#
################################

from flask import render_template, flash, redirect, url_for, request, send_from_directory    
from app import app, db, photos
from sqlalchemy import func
from app.forms import LoginForm, RegistrationForm, NewPostForm, MessageForm, \
     DeletePostForm, ApprovePostForm
from app.models import User, Post, Message, Category
from flask_login import current_user, login_user, login_required, logout_user
from flask_paginate import Pagination, get_page_args
from werkzeug.urls import url_parse
from werkzeug import secure_filename
import hashlib
import os

######################
# Utility Functions  #
######################

def get_paginated_posts(posts, offset=0, per_page=5):
    return posts[offset: offset + per_page]

def get_category():
    return Category.query.all()

#################
# End Utilities #
#################

# renders the homepage and links the login_modal to the form
@app.route('/')
def index():
    login_form = LoginForm()
    posts = Post.query.filter_by(active=True).order_by(Post.timestamp.desc()).limit(5).all()
    return render_template('index.html', title="Home", login_form=login_form, category=get_category(), posts=posts)

# renders about page
@app.route('/about')
def about():
    login_form = LoginForm()
    return render_template('about.html', title="About", login_form=login_form, category=get_category())

# renders privacy policy page
@app.route('/tos')
def privacypolicy():
    login_form = LoginForm()
    return render_template('privacypolicy.html', title="About", login_form=login_form, category=get_category())

# search results page
@app.route('/search/', methods=['GET', 'POST'])
def search():
    login_form = LoginForm()
    if request.method == "POST":
        selected_category = request.form["category"]
        query = request.form["search"]
        # get category_id from dropdown
        category_in_db = Category.query.filter_by(name=str(selected_category)).first()
        search = '%{}%'.format(query)
        # if no search category changed/All category
        if category_in_db.name != "All":
            posts = Post.query.filter(Post.title.like(search).filter(Post.category.like(category_in_db.id))).filter_by(active=True)
        # else query specific category
        else: 
            posts = Post.query.filter(Post.title.like(search)).filter_by(active=True).all()
        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        per_page = 100
        total_posts = len(posts)
        if total_posts == 0:
            posts = Post.query.filter(Post.category.like(category_in_db.id)).filter_by(active=True).all()
        pagination_posts = get_paginated_posts(posts, offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=total_posts, css_framework='bootstrap4', record_name="results")
        return render_template('search.html', login_form=login_form , query=query, category=get_category(), \
                posts=pagination_posts, page=page, per_page=per_page, pagination=pagination, total_posts= total_posts)
    else: 
        # handles direct request to /search page without entering in search bar
        posts = Post.query.filter().filter_by(active=True).all()
        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        per_page=5
        total_posts = len(posts)
        pagination_posts = get_paginated_posts(posts, offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=total_posts, css_framework='bootstrap4', record_name="results")
        return render_template('search.html', login_form=login_form, category=get_category(), \
                posts=pagination_posts, page=page, per_page=per_page, pagination=pagination, total_posts=total_posts)



# Checks if user is logged in and returns to original page. 
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if login_form.validate_on_submit():
            user = User.query.filter_by(email=login_form.email.data).first()
            if user is None or not user.check_password(login_form.password.data):
                flash('Incorrect Password or Username')
                return redirect(url_for('login'))
            login_user(user, remember=login_form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login.html', title='Sign In', login_form=login_form, category=get_category())

# link to registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm()
    register_form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if register_form.validate_on_submit():
        user = User(email=register_form.email.data)
        user.set_password(register_form.password.data)
        user.set_username()
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', login_form=login_form, register_form=register_form, category=get_category())

# logs out and takes to home page
@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# links to form to create a post
@login_required
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    login_form = LoginForm()
    new_post_form = NewPostForm()
    if new_post_form.validate_on_submit():
        if current_user.is_authenticated:
            selected_category = Category.query.filter_by(name=str(new_post_form.category.data)).first()
            new_post_price = "$%.2f" % new_post_form.price.data
            print(new_post_price)
            if new_post_form.image.data is not None: 
                filename = hashlib.md5(str(new_post_form.image.data.filename).encode('utf-8')).hexdigest()
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                new_post_form.image.data.save(file_path)
                post = Post(title=new_post_form.title.data, body=new_post_form.body.data, user_email=current_user.email, category=selected_category.name, image=filename, price=new_post_price)
            else:
                post = Post(title=new_post_form.title.data, body=new_post_form.body.data, user_email=current_user.email, category=selected_category.name, price=new_post_price)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been made! Please wait at least 24 hours for it to go live.')
            return redirect(url_for('index'))
        else: 
            return redirect("login")
    return render_template("create_post.html", title="Create Post", login_form=login_form, new_post_form=new_post_form, category=get_category())

@login_required
@app.route('/post/<int:post_id>/delete_post/', methods=['GET', 'POST'])
def delete_post(post_id):
    login_form = LoginForm()
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post.User.id == current_user.id:
        delete_post_form = DeletePostForm()
        if delete_post_form.validate_on_submit():
            if delete_post_form.radio.data == "yes":
                Post.query.filter_by(id=post_id).delete()
                db.session.commit()
                flash('Post deleted!')
            return redirect(url_for('user', username=current_user.username))
        return render_template("delete_post.html", delete_post_form=delete_post_form, category=get_category(), login_form=login_form )
    return redirect(url_for('view_post', post_id=post_id))

@login_required
@app.route('/post/<int:post_id>/approve_post/', methods=['GET', 'POST'])
def approve_post(post_id):
    login_form = LoginForm()
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post.User.id == current_user.id:
        approve_post_form = ApprovePostForm()
        if approve_post_form.validate_on_submit():
            if approve_post_form.radio.data == "yes":
                post.active = True
                db.session.commit()
                flash('Post approved!')
            else: 
                post.active=False
                db.session.commit()
                flash('Post Hidden!')
            return redirect(url_for('user', username=current_user.username))
        return render_template("approve_post.html", approve_post_form=approve_post_form, category=get_category(), login_form=login_form )
    return redirect(url_for('view_post', post_id=post_id))
    
# routing for unique user pages. 
@login_required
@app.route('/user/<username>')
def user(username):
    login_form = LoginForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_email=user.email)
    num_posts = 0
    for post in posts:
        num_posts += 1
        if current_user.admin == True:
            user_list = User.query.filter().all()
            post_list = Post.query.filter().all()
            return render_template('user.html', user=user, posts=posts, num_posts=num_posts, login_form=login_form, category=get_category(), user_list = user_list, post_list=post_list)
    return render_template('user.html', user=user, posts=posts, num_posts=num_posts, login_form=login_form, category=get_category())
   


# routing for unique post pages.
@app.route('/post/<post_id>/')
def view_post(post_id):
    login_form=LoginForm()
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('post.html', post=post, login_form=login_form, category=get_category())

# method to return images from directory 
@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# message form for posts
@login_required
@app.route('/post/<id>/send_message/', methods=['GET', 'POST'])
def send_message(id):
    login_form = LoginForm()
    message_form = MessageForm()
    post = Post.query.filter_by(id=id).first_or_404()
    if message_form.validate_on_submit():
        message = Message(post=id, sender_name=current_user.username, recipient_id=post.user.id, body=message_form.body.data)
        db.session.add(message)
        db.session.commit()
        flash('Message has been sent to sender!')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('view_post', login_form=login_form, message_form=message_form, post_id=id, )
        return redirect(next_page)
    return render_template('send_message.html', id=id, login_form=login_form, message_form=message_form, post=post, category=get_category())

