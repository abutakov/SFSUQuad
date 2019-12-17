#!/usr/bin/env python3

################################
#         __init__.py          #
# Main website routing/control #
# Created by Andrew Copas      #
# Modified by:                 #
# Emanuel Saunders(Nov 10,2019)#
################################


from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_thumbnails import Thumbnail
from flask_paginate import Pagination, get_page_args

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app) # default is 16 MB, to set use ...(app, 32 * 1024 * 1024 )

thumb = Thumbnail(app)

from app import routes, models
