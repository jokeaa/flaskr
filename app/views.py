from app import app,db,lm,oid
from flask import render_template,flash,redirect,session,url_for,request,g
from flask_login import login_user,logout_user,current_user,login_required
from .forms import LoginForm
from .models import User

@lm.user_loader
def load_user(id):
    users = User.query.get(int(id))
    print users
    return users

@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user

    posts = [
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',title = 'Home',user=user,posts=posts)



@app.route('/login',methods=['GET','POST'])
@oid.loginhandler
def login():
    form = LoginForm()
    if g.user is not None and g.user.is_authenticated:
            return redirect(url_for('index'))
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        if form.login_type.data == 'id_login':
            return oid.try_login(form.openid.data,ask_for=['nickname','email'])
        else:
            pass

    return render_template(
            'login.html',
            title = 'Sign In',
            form = form,
            providers = app.config['OPENID_PROVIDERS']
        )
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login.Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname,email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me',None)
    login_user(user,remember=remember_me)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))