#!/usr/bin/env python2.7
## @file
## @brief kiosk web server (local http only)

## @defgroup kiosk
## @brief local web server (http only)
## @{

from forth import *

import os,sys
import flask,flask_wtf,wtforms

web = flask.Flask(__name__)

web.config['SECRET_KEY'] = os.urandom(32)

class CmdForm(flask_wtf.FlaskForm):
    error = wtforms.StringField('no error')
    pad   = wtforms.TextAreaField('pad')
    go    = wtforms.SubmitField('GO')
    
@web.route('/', methods=['GET', 'POST'])
def index():
    form = CmdForm()
    if form.validate_on_submit(): F.push(String(form.pad.data)) ; INTERPRET(F)
    return flask.render_template('index.html', form=form, \
                                vm=F.dump(slots=False), plan=F['plan'].dump())

@web.route('/<sym>')
def dump(sym):
    return flask.render_template('dump.html',dump=F[sym].dump())

web.run(debug=True,host='127.0.0.1',port=8888)

## @}
