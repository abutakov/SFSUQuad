#!/usr/bin/env python3

################################
#         App.py               #
# Main website routing/control #
# Created by Andrew Copas      #
# Modified by:                 #
# Emanuel Saunders(Nov 10,2019)#
################################

from flask import Flask, render_template, request, redirect, session, url_for
from flaskext.mysql import MySQL
from flask_thumbnails import Thumbnail
from werkzeug.urls import url_parse
import re

app = Flask(__name__, static_url_path='/var/www/html/static', static_folder='static', template_folder='templates')

# Thumbnail extension config
thumb = Thumbnail(app)
app.config['THUMBNAIL_MEDIA_ROOT'] = '/var/www/html/static/user_images'
app.config['THUMBNAIL_MEDIA_URL'] = '/user_images/'
app.config['THUMBNAIL_MEDIA_THUMBNAIL_ROOT'] = '/var/www/html/static/user_images/cache'
app.config['THUMBNAIL_MEDIA_THUMBNAIL_URL'] = '/var/www/html/static/user_images/cache/'
app.config['THUMBNAIL_STORAGE_BACKEND'] = 'flask_thumbnails.storage_backends.FilesystemStorageBackend'
app.config['THUMBNAIL_DEFAUL_FORMAT'] = 'JPEG'

# Secret Key
app.secret_key = 'your secret key'

# Connect to the MySQL database
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'prototypedb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)

@app.route('/ourTeam')
def outTeam():
    return render_template('about.html')


@app.route('/about_Alex')
def alexProfile():
    return render_template('about_team_members/about_Alex.html')


@app.route('/about_AlexLee')
def alexLeeProfile():
    return render_template('about_team_members/about_AlexLee.html')


@app.route('/about_Andrew')
def andrewProfile():
    return render_template('about_team_members/about_Andrew.html')


@app.route('/about_Emanuel')
def emanuelProfile():
    return render_template('about_team_members/about_Emanuel.html')


@app.route('/about_Kevin')
def kevinProfile():
    return render_template('about_team_members/about_Kevin.html')


@app.route('/about_Tim')
def timProfile():
    return render_template('about_team_members/about_Tim.html')

@app.route('/admin_dash')
def adminDash():
    return render_template('admin_dash.html')

@app.route('/user_dash')
def userDash():
    return render_template('user_dash.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = mysql.connect()
    cursor = conn.cursor()
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM users WHERE username = %s AND BINARY password = %s', (username, password))
        users = cursor.fetchone()
        if users:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = users[0]
            session['username'] = users[1]
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))
    
@app.route('/vp', methods=['GET', 'POST'])
def verticalproto():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name from categories ORDER BY name ASC")
    conn.commit()
    cats = cursor.fetchall()
    if request.method == "POST":
        category = request.form['category']
        item = request.form['item']
        query = item
        # all in the search box will return all the tuples
        if len(item) == 0:
            if category == "All":
                cursor.execute("SELECT P.title, P.description, C.name, P.image FROM posts P, categories C WHERE P.category=C.cID")
                conn.commit()
                data = cursor.fetchall()
            else:
                cursor.execute("SELECT P.title, P.description, C.name, P.image FROM posts P, categories C WHERE P.category = C.cID AND C.name = '%s'" %(category))
                conn.commit()
                data = cursor.fetchall()
        # search by category
        else:
            if category == "All":
                cursor.execute("SELECT P.title, P.description, C.name, P.image FROM posts P JOIN categories C ON P.category = C.cID WHERE P.description LIKE '%%%s%%' OR P.title LIKE '%%%s%%'" %(item, item))
                conn.commit()
                data = cursor.fetchall()
            else:
                cursor.execute("SELECT P.title, P.description, C.name, P.image FROM posts P JOIN categories C ON P.category = C.cID WHERE C.name = '%s' AND (P.description LIKE '%%%s%%' OR P.title LIKE '%%%s%%')" %(category, item, item))
                conn.commit()
                data = cursor.fetchall()
            conn.close()
        return render_template('verticalproto.html', query=query, data=data, cats=cats)
    conn.close()
    return render_template('verticalproto.html', cats=cats)

@app.route('/', methods=['GET', 'POST'])
def search():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name from categories ORDER BY name ASC")
    conn.commit()
    cats = cursor.fetchall()
    if request.method == "POST":
        category = request.form['category']
        item = request.form['item']
        query = item
        # all in the search box will return all the tuples
        if len(item) == 0:
            if category == "All":
                cursor.execute("SELECT P.title, P.description, C.name, P.image FROM posts P, categories C WHERE P.category=C.cID")
                conn.commit()
                data = cursor.fetchall()
            else:
                cursor.execute("SELECT P.title, P.description, C.name, P.image FROM posts P, categories C WHERE P.category = C.cID AND C.name = '%s'" %(category))
                conn.commit()
                data = cursor.fetchall()
        # search by category
        else:
            if category == "All":
                cursor.execute("SELECT P.title, P.description, C.name, P.image FROM posts P JOIN categories C ON P.category = C.cID WHERE P.description LIKE '%%%s%%' OR P.title LIKE '%%%s%%'" %(item, item))
                conn.commit()
                data = cursor.fetchall()
            else:
                cursor.execute("SELECT P.title, P.description, C.name, P.image FROM posts P JOIN categories C ON P.category = C.cID WHERE C.name = '%s' AND (P.description LIKE '%%%s%%' OR P.title LIKE '%%%s%%')" %(category, item, item))
                conn.commit()
                data = cursor.fetchall()
            conn.close()
        return render_template('search.html', query=query, data=data, cats=cats)
    conn.close()
    return render_template('index.html', cats=cats)

if __name__ == '__main__':
    #  app.run(host="0.0.0.0", port=80, debug=True)
    app.run(host="localhost", port=5000, debug=True)