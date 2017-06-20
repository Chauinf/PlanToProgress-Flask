from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_uploads import UploadSet, configure_uploads, patch_request_class, ALL
import config
import os

app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOADED_DEFAULT_DEST'] = os.getcwd() + '/uploads/'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

file_upload = UploadSet('default', ALL)
configure_uploads(app, file_upload)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

from . import views, models, forms
