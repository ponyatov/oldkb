# Marvin Minsky Frame computation model
## based on attributed object graphs
### in Python

import os, sys, re, pickle
from __builtin__ import isinstance

##################### frame class system #################

# base Frame class
class Frame:

    # construct with given name
    def __init__(self, V):
        
        # type/class tag
        self.type = self.__class__.__name__.lower()
        
        # primitive value (implementation language type)
        self.value = V
        
        # attributes = named slots
        self.attr = {}
        
        # nested elements = ordered slots = AST & syntax trees for CL parsing
        self.nest = []
        
    # set named slot to other frame
    def __setitem__(self, key, frame):
        if isinstance(frame, Frame):
            self.attr[key] = frame
        else:
            self.attr[key] = Frame(frame)
        return self
    
    # get slot value by name
    def __getitem__(self, key):
        if isinstance(key, Frame):
            return self.attr[key.value]
        else:
            return self.attr[key]

    # << operator    
    def __lshift__(self, frame):
        return self.push(frame)
    
    # push ordered/stack
    def push(self,frame):
        if isinstance(frame, Frame):
            self.nest.append(frame)
        elif isinstance(frame,str) and re.match(r'^http',frame):
            self.nest.append(URL(frame))
        else:
            self.nest.append(Frame(frame))

    # print frame in human readable form
    def __repr__(self):
        return self.dump()
    
    # represent any frame/object in html
    def html(self):
        return self.dump()
    # plot object via D3.js
    def plot(self):
        return self.value
    
    # dump in full tree
    dumped = []
    def dump(self, depth=0, prefix=''):
        S = self.pad(depth) + self.head(prefix)
        if not depth: Frame.dumped = []
        if self in Frame.dumped: return S + ' ...'
        else: Frame.dumped.append(self)
        for i in self.attr:
            S += self.attr[i].dump(depth + 1, prefix='%s = ' % i)
        for j in self.nest:
            S += j.dump(depth + 1)
        return S
    
    # dump in short header-only form
    def head(self, prefix=''):
        return '%s<%s:%s>' % (prefix, self.type, self.value)
    
    # left pad with tabs for tree dump
    def pad(self, N):
        return '\n' + '\t' * N
    
################# generic programming ##############

class Container(Frame): pass

# LIFO stack
class Stack(Container): pass

# vocabulary ( map, associative array )
class Voc(Frame):
    
    # << operator    
    def __lshift__(self, frame):
        if isinstance(frame,Frame):
            self[frame.value] = frame
        else:
            self.push(Frame(frame))

####################### global vocabulary ###################

# global vocabulary
W = Voc('global')

# load from .db
def LOAD():
    global W
    try:    F = open(sys.argv[0] + '.db', 'r') ; W = pickle.load(F) ; F.close()
    except: pass
    
# save to .db
def SAVE():
    pickle.dump(W, open(sys.argv[0] + '.db', 'w'))
    
########################## data stack #######################

S = Stack('data')

################# Dumb FORTH-like interpreter ###########

import ply.lex  as lex      # no syntax parser, lexer only

tokens = ['frame']

t_ignore = ' \t\r\n'

def t_frame(t):
    r'[a-zA-Z0-9_\+\-\*\/\:\;\?\.\:\;\<\>\(\)]+'
    return Frame(t.value)

def t_error(t):
    raise SyntaxError(t)

lexer = lex.lex()

def INTERPRET(SRC):
    lexer.input(SRC)
    while True:
        token = lexer.token()
        if not token: break
        try:
            S << W[token]
        except KeyError:
            S << token

######################### Internet ######################

class URL(Frame): pass

####################### Web interface ###################

import flask, flask_wtf, wtforms

web = flask.Flask(__name__)

web.config['SECRET_KEY'] = os.urandom(32)

class Form(flask_wtf.FlaskForm):
    ## error message
    error = wtforms.StringField('no error')
    ## FORTH code entry
    pad = wtforms.TextAreaField('pad')
    ## go button
    go  = wtforms.SubmitField('GO')


# main page route
@web.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    if form.validate_on_submit(): INTERPRET(form.pad.data)
    return flask.render_template('index.html', form=form, S=S.dump(), W=W.dump())

# vocabulary dump by single name
@web.route('/dump/<frame>', methods=['GET', 'POST'])
def dumpX(frame):
    form = Form()
    if form.validate_on_submit(): INTERPRET(form.pad.data)
    return flask.render_template('dump.html', form=form, dump = W[frame].dump())

# vocabulary element vizualization by single name
@web.route('/plot/<frame>', methods=['GET', 'POST'])
def plotX(frame):
    form = Form()
    if form.validate_on_submit(): INTERPRET(form.pad.data)
    return flask.render_template('plot.html', \
                    form=form, dump = W[frame].dump(), plot = W[frame].plot() )

#############################################################

# marvin = Frame('marvin')
# marvin['first_name'] = 'Marvin'
# marvin['last_name' ] = 'Minsky'
# marvin << 'https://en.wikipedia.org/wiki/Marvin_Minsky'
# W << marvin
# SAVE()

################# build base vocabulary ##################

W['W'] = W
W['S'] = S
# SAVE()

######################### startup ########################

# autoload on system startup
# LOAD()

if __name__ == '__main__':
    web.run(debug=True,host='127.0.0.1',port=2345)
