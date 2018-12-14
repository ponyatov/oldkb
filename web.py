#!/usr/bin/env python2.7

## @file
## @brief Web interface /Flask/

## @defgroup interactive interactive
## @brief interfaces

## @defgroup web Web interface
## @ingroup interactive 
## @brief Flask-based: full-sized http/https, user authorization
## @{ 

from forth import *

import os,sys
import flask,flask_wtf,wtforms

## Flask application
app = flask.Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)

import flask_login
## user login manager plugin for Flask
logman = flask_login.LoginManager() ; logman.init_app(app)

from secrets import IP,PORT
from secrets import LOGIN_HASH, PSWD_HASH 
# openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
from secrets import SSL_KEYS

try:
    for i in SSL_KEYS: open(i,'r').close()
except IOError:
    ## disable SSL
    SSL_KEYS = None
    ## force local host only
    IP = '127.0.0.1'
    ## enable rich debug info on errors
    DEBUG = True

from werkzeug.security import generate_password_hash,check_password_hash

## command entry form
class CmdForm(flask_wtf.FlaskForm):
    ## error indicator line
    error = wtforms.StringField('no error')
    ## command entry text field
    pad   = wtforms.TextAreaField('pad')
    ## go button
    go    = wtforms.SubmitField('GO')

##
@app.route('/', methods=['GET', 'POST'])
## index route
def index():
    if not flask_login.current_user.is_authenticated:
        return flask.redirect('/login')
    form = CmdForm()
    if form.validate_on_submit(): F.push(String(form.pad.data)) ; INTERPRET(F)
    return flask.render_template('index.html', form=form, F=F)

## web user for https login
class User(flask_login.UserMixin):
    ## construct user with
    ## @param id
    def __init__(self,id):
        ## user id
        self.id = id
@logman.user_loader
## user loader callback
def load_user(user_id): return User(user_id) 

## login form
class LoginForm(flask_wtf.FlaskForm):
    ## login field
    login = wtforms.StringField('login', [wtforms.validators.DataRequired()])
    ## password field
    pswd  = wtforms.PasswordField('password', [wtforms.validators.DataRequired()])
    ## go button
    go    = wtforms.SubmitField('GO')

##
@app.route('/login', methods = ['GET', 'POST'])
## login page route
def login():
    flask_login.logout_user()
    form = LoginForm()
    if form.validate_on_submit():
        LOGIN = form.login.data
        PSWD  = form.pswd.data
        if  check_password_hash(LOGIN_HASH, form.login.data) \
        and check_password_hash(PSWD_HASH , form.pswd.data ):
            flask_login.login_user(User(LOGIN))
            return flask.redirect('/')
        else:
            print 'LOGIN_HASH',generate_password_hash(LOGIN)
            print 'PSWD_HASH' ,generate_password_hash(PSWD)
            return flask.redirect('/login')
    return flask.render_template('login.html',form=form)

@app.route('/logout')
@flask_login.login_required
def logout(): flask.redirect('/login')

## dump any object by `/sym` route
@app.route('/<sym>')
@flask_login.login_required
def dump(sym):
    return flask.render_template('dump.html',dump=F[sym].dump())

if __name__ == '__main__':
    ## @param host IP address or `0.0.0.0` for all
    ## @param post IP port
    ## @param debuf extended debug info via web for Python errors
    ## @param ssl_context HTTPS 
    app.run(debug=True, host=IP, port=PORT, ssl_context = SSL_KEYS)

## @}
