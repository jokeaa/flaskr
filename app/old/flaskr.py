from flask import Flask, render_template,flash
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.debug = True

app.config['SECRET_KEY'] = 'this_is_a_session_key'
app.config.from_envvar('FLASKR_SETTINGS',silent=True)
toolbar = DebugToolbarExtension(app)

@app.route('/')
def hello_world():
    flash('try the flash')
    return render_template('test.html')





if __name__ == '__main__':
    app.run()
