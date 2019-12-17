#!/usr/bin/env python3

################################
#         config.py            #
# environment vars/backend     #
# Modified by:                 #
# Emanuel Saunders(Nov 10,2019)#
################################

import os
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = 'teameight'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'teameight'
    # TODO: fix database url here: (mysql://user:pass@server/db)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:zonmin678@localhost/app'        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'uploads')
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
