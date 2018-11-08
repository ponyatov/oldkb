# Marvin Minsky Frame computation model
## based on attributed object graphs
### in Python

import os, sys, re, pickle

##################### frame class system #################

# base Frame class
class Frame:

    # construct with given name
    def __init__(self, V):
        
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
    
    # dump in full tree
    def dump(self, depth=0, prefix=''):
        S = self.pad(depth) + self.head(prefix)
        for i in self.attr:
            S += self.attr[i].dump(depth + 1, prefix='%s = ' % i)
        for j in self.nest:
            S += j.dump(depth + 1)
        return S
    
    # dump in short header-only form
    def head(self, prefix=''):
        return '%s<%s:%s>' % (prefix, self.__class__.__name__.lower(), self.value)
    
    # left pad with tabs for tree dump
    def pad(self, N):
        return '\n' + '\t' * N
    
################# generic programming ##############

class Container(Frame): pass

# LIFO stack
class Stack(Container): pass

# vocabulary ( map, associative array )
class Voc(Frame): pass

####################### global vocabulary ###################

W = Voc('global')

# load from .db
def LOAD():
    global W
    try:    F = open(sys.argv[0] + '.db', 'r') ; W = pickle.load(F) ; F.close()
    except: pass
    
# autoload on system startup
LOAD()

# save to .db
def SAVE():
    pickle.dump(W, open(sys.argv[0] + '.db', 'w'))
    
    
########################## data stack #######################

S = Stack('DATA')

####################### Internet ###################

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

@web.route('/', methods=['GET', 'POST'])
def index():
    return flask.render_template('index.html',form=Form(),S=S.dump())

######################### startup ########################

if __name__ == '__main__':
    web.run(debug=True,host='127.0.0.1',port=2345)

#############################################################

# marvin = Frame('marvin')
# marvin['first_name'] = 'Marvin'
# marvin['last_name' ] = 'Minsky'
# marvin << 'https://en.wikipedia.org/wiki/Marvin_Minsky'
# # W << marvin
# # SAVE()

print W
