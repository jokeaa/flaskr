from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    openid = StringField('openid',validators=[DataRequired()])
    remember_me = BooleanField('remember_me',default=False)
    login_type = SelectField('login_type',
                             choices=[('id_login','id_login'),('username_login','username_login')],
                             validators=[DataRequired()]
                             )