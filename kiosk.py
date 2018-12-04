#!/usr/bin/env python2.7
## @file
## @brief kiosk web server (local http only)

## @defgroup kiosk
## @brief local web server (http only)
## @{

from forth import *

import os,sys
import flask,flask_wtf,wtforms,werkzeug

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)

class CmdForm(flask_wtf.FlaskForm):
    error = wtforms.StringField('no error')
    pad   = wtforms.TextAreaField('pad')
    go    = wtforms.SubmitField('GO')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CmdForm()
    if form.validate_on_submit(): F.push(String(form.pad.data)) ; INTERPRET(F)
    return flask.render_template('index.html', form=form, F=F)

@app.route('/<sym>')
def dump(sym):
    return flask.render_template('dump.html',dump=F[sym].dump())

app.config['MAX_CONTENT_LENGTH'] = 2 << 10

@app.route('/upload', methods=['GET','POST'])
def upload():
    if flask.request.method == 'POST':
        print flask.request.files
        file = flask.request.files['file'] ; print 'file',file
        name = werkzeug.utils.secure_filename(file.filename) ; print 'name',name
        if not name: return flask.redirect(flask.request.url)
        mime = file.mimetype
        print 'mime',mime
        if mime == 'application/octet-stream':
            F.push ( pickle.loads(file.read()) )
        return flask.redirect('/')
    return flask.render_template('upload.html',S=F.dump(slots=False))

app.run(debug=True,host='127.0.0.1',port=8888)

## @}
