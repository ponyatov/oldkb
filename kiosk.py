#!/usr/bin/env python2.7

import os,sys

import flask,flask_wtf,wtforms

web = flask.Flask(__name__)

web.config['SECRET_KEY'] = os.urandom(32)

class CmdForm(flask_wtf.FlaskForm):
    error = wtforms.StringField('no error')
    pad   = wtforms.TextAreaField('pad')
    go    = wtforms.SubmitField('GO')
    
vm = {}

@web.route('/', methods=['GET', 'POST'])
def index():
    form = CmdForm()
    if form.validate_on_submit(): vm['command'] = form.pad.data
    return flask.render_template('index.html',form=form,vm=vm)

web.run(debug=True,host='127.0.0.1',port=8088)
