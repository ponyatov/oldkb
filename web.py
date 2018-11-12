
from forth import *

import os
import flask,flask_wtf,wtforms

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)

IP = '0.0.0.0'

PORT = 8888

class CmdForm(flask_wtf.FlaskForm):
    error = wtforms.StringField('no error')
    pad   = wtforms.TextAreaField('pad')
    go    = wtforms.SubmitField('GO')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CmdForm()
    return flask.render_template('index.html', form=form, vm='<vm:FORTH>')

if __name__ == '__main__':
    app.run(debug=True, host=IP, port=PORT)#, ssl_context = SSL_KEYS)
