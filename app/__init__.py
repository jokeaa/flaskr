from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir,ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD,LOG_TYPE

import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app,os.path.join(basedir,'temp'))


from app import views,models

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler,RotatingFileHandler

    if LOG_TYPE == 'email':
        credentials = None
        if MAIL_USERNAME or MAIL_PASSWORD:
            credentials = (MAIL_USERNAME,MAIL_PASSWORD)
        #mail_handler = SMTPHandler((MAIL_SERVER,MAIL_PORT), MAIL_SERVER,ADMINS, 'microblog failure', credentials)
        mail_handler = SMTPHandler(
            'smtp.qq.com', MAIL_USERNAME,ADMINS, 'microblog failure', credentials,
            secure=()

        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    else:
        file_handler = RotatingFileHandler('temp/microblog.log','a',1*1024*1024,10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('microblog startup')

