from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir

import os

app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
oid = OpenID(app,os.path.join(basedir,'temp'))

db = SQLAlchemy(app)
from app import views,models
