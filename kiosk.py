#!/usr/bin/env python2.7
## @file
## @brief kiosk web server (local http only)

## @defgroup kiosk
## @ingroup web
## @brief local web server (light http only)
## @{

from forth import *

import os,sys
import flask,flask_wtf,wtforms,werkzeug

## Flask application
app = flask.Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)

from web import CmdForm

## @param methods
@app.route('/', methods=['GET', 'POST'])
## `/` index route
def index():
    form = CmdForm()
    if form.validate_on_submit(): F.push(String(form.pad.data)) ; INTERPRET(F)
    if 'plan' in F['web'].keys(): plan = F['plan'].dump(header=False)
    else: plan =''
    if 'words' in F['web'].keys(): words = F.slots().value
    else: words=''
    return flask.render_template('index.html', form=form, F=F, plan=plan, words=words)

## dump any object by `/sym` route
@app.route('/<path:sym>')
def dump(sym):
    R = F
    # iterate over slashed path
    for i in sym.split('/'): R=R[i]
    return flask.render_template('dump.html',dump=R.dump())

app.config['MAX_CONTENT_LENGTH'] = 2 << 10

@app.route('/upload', methods=['GET','POST'])
## `/upload` route
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
