#!/usr/bin/env python2.7

## @file
## @brief engine

import os,sys,pickle,types

## @defgroup sym symbolic class system
## @{

## base object
class Object:
    
    ## constructor 
    def __init__(self,V):
        ## type/class tag
        self.type = self.__class__.__name__.lower()
        ## single primitive value
        self.value = V
        ## nest[]ed objects can run both as stack and ordered vector
        self.nest = []
        ## attr{}ibutes can be used for associative array or class slots
        self.attr = {}
        
    ## @defgroup dump print/dump
    ## @brief text representation for any object
    ## @{
    
    ## return text representation for any object
    def __repr__(self):
        return self.dump()
    ## dump in full tree form
    ## @param[in] depth tree padding
    ## @param[in] prefix prefix string before first line of subtree
    def dump(self,depth=0,prefix=''):
        S = self.pad(depth) + self.head(prefix)
        for i in self.attr:
            S += self.attr[i].dump(depth+1,prefix='%s = '%i)
        for j in self.nest:
            S += j.dump(depth+1)
        return S
    ## dump in short header-only form
    def head(self,prefix=''):
        return '%s<%s:%s> @%X' % (prefix, self.type, self.str(), id(self))
    ## string representation of value only w/o special formats
    def str(self):
        return str(self.value)
    ## left padding
    def pad(self,N):
        return '\n'+'\t'*N
    
    ## @}
    
    ## @defgroup symstack stack operations
    ## @ingroup cont
    ## @{
    
    ## @brief push nested object 
    def push(self,obj): self.nest.append(obj) ; return self
    ## @brief pop nested object
    def pop(self): return self.nest.pop()
    ## @brief get top of stack without removing
    def top(self): return self.nest[-1]
    ## @brief clear stack
    def clear(self): self.nest = []
    ## @}
    
    ## @defgroup symmap map operations
    ## @ingroup cont
    ## @{
    
    ## fetch attribute value
    ## @param[in] key
    def __getitem__(self,key): return self.attr[key]
    ## store to attribute
    ## @param[in] key
    ## @param[in] obj
    def __setitem__(self,key,obj): self.attr[key] = obj ; return self
    ## @}

## @defgroup prim primitive
## @brief close to machine level or implementation language types (Python)
## @{

## primitive object
class Primitive(Object): pass

## @defgroup symbol symbol
## @brief names variables and other objects
## @{

## symbol (names variables and other objects)
class Symbol(Primitive): pass

## @}

## @defgroup string string 
## @{

## string
class String(Object): pass

## @}

## @defgroup nums numbers
## @{

## floating pointer number
class Number(Primitive):
    ## construct with `float(value)`
    def __init__(self,V):
        Primitive.__init__(self, float(V))

## integer number
class Integer(Number):
    ## construct with `integer(value)`
    def __init__(self,V):
        Primitive.__init__(self, int(V))
        
## hexadecimal machine number
class Hex(Integer): 
    ## construct from `0xDeadBeef`
    def __init__(self,V):
        Primitive.__init__(self, int(V[2:],0x10))
    ## represent in `0xNNNN` form
    def str(self):
        return '0x%X' % self.value

## binary vector
class Bin(Integer): 
    ## construct from `0b1101`
    def __init__(self,V):
        Primitive.__init__(self, int(V[2:],0x02))
    ## represent in `0b1101` form
    def str(self):
        return bin(self.value)

## @}    

## @}

## @defgroup cont data container
## @brief any object in @ref sym can be used as stack, vector and map
## @{

## data container
class Container(Object): pass

## LIFO stack
class Stack(Container): pass

## associative array
class Map(Container):
    ## shift object both into `attr{}` and `nest[]`ed
    def __lshift__(self,obj):
        if type(obj) is types.FunctionType:
            self.attr[obj.__name__] = Fn(obj)
        else:
            self.attr[obj.value] = obj

## ordered vector
class Vector(Container): pass

## @}

## @defgroup active active element
## @brief has execution semantics
## @{

## active element has execution semantics
class Active(Object): pass

## python function wrapper
class Fn(Active):
    ## construct wrapper
    ## @param[in] F python function `void noreturn()`
    def __init__(self,F):
        Active.__init__(self, F.__name__)
        ## function holder
        self.fn = F
    ## call object
    def __call__(self): self.fn()
    
## operator
class Op(Active): pass

## virtual machine
class VM(Active): pass

## @}

## @defgroup meta meta
## @{

class Meta(Object): pass

## @defgroup class class
## @brief OOP abstractions
## @{

## class is an abstract @ref Object
class Class(Meta): pass

## group of messages understandable by some @ref Class
class Interface(Meta): pass 

## @}

## @defgroup lang lang
## @brief computer-oriented language (programming, markup, description,..)
## @{

## computer-oriented language (programming, markup, description,..)
class Lang(Meta): pass

## @}

## @}

## @defgroup deploy deploy
## @brief target deploy environments and platforms for software synthesys
## @{

class Deploy(Object): pass

## @defgroup hw hardware
## @brief architecture and computing hardware
## @{

## hardware component
class HW(Deploy): pass

## processor/SoC/MCU arhitecture
class ARCH(HW): pass

## processor/SoC/MCU core
class CPU(HW): pass 

## @}

## @defgroup os os
## @brief operating system
## @{

class OS(Deploy): pass

## @defgroup fw framework
## @brief multi-platform high-level OS abstraction
## @{

## multi-platform high-level OS abstraction
class Framework(Deploy): pass

## @}

## @}

## @defgroup compiler compiler
## @brief compiler/interpreter for @ref lang
## @{

## generic compiler/interpreter
class Compiler(Deploy): pass

## C compiler
class CC(Compiler): pass

## C++ compiler

class CXX(CC): pass

## Assembler
class AS(Compiler): pass

## @}

## @}

## @}

## @defgroup doc documenting
## @brief not only program documentation but any generic docs
## @{

## documentation element
class Doc(Object): pass

## @defgroup html HTML
## @brief most portable format *required for this **online** system*
## @{

## .html document element
class HTML(Doc): pass

## @}

## @}

## @defgroup fvm FORTH VM
## @{

## @defgroup stack data stack
## @{

## global data stack
S = Stack('DATA')

## @}

## @defgroup voc global vocabulary
## @{ 

## global vocabulary
W = Map('FORTH')

## load vocabulary from persistent image (pickle)
def LOAD():
    global W
    try: F = open(sys.argv[0]+'.db','r') ; W = pickle.load(F) ; F.close()
    except: pass
W << LOAD
LOAD()

## save vocabulary to pickle image
def SAVE():
    global W
    F = open(sys.argv[0]+'.db','w') ; pickle.dump(W, F) ; F.close()
W << SAVE
# SAVE()

## @}

## @defgroup deb debug
## @{

## `?? ( -- )` \ dump @ref fvm state
def qq():
    print W ; print S
W['??'] = Fn(qq)

## `? ( -- )` \ print @ref stack only
def q():
    print S
W['?'] = Fn(q)

## `. ( ... -- )` \ clear data stack
def dot():
    S.clear()
W['.'] = Fn(dot)

## @}

## @}

## @defgroup interp Interpreter
## @{

## @defgroup syntax syntax parser
## @brief powered with PLY library
## @{

import ply.lex  as lex  # FORTH has no syntax we need lexer only

## token types list
## @details @ref sym
## * follows API of PLY library with object `type`/`value`
## * in result we able to directly use @ref prim s as tokens
## * and should use lowercased class names here
tokens = ['symbol','string','number','integer','hex','bin']

## drop spaces
t_ignore = ' \t\r'

## line comments
def t_ignore_COMMENT(t):
    r'[#\\].*'

## count line number
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
## hexadecimal
def t_hex(t):
    r'0x[0-9a-fA-F]+'
    return Hex(t.value)
    
## binary
def t_bin(t):
    r'0b[01]+'
    return Bin(t.value)
    
## exponential with integer base
def t_number_exp(t):
    r'[\+\-]?[0-9]+[eE][\+\-]?[0-9]+'
    return Number(t.value)
    
## floating point number token
def t_number(t):
    r'[\+\-]?[0-9]+\.[0-9]*([eE][\+\-]?[0-9]+)?'
    return Number(t.value)
    
## integer number token
def t_integer(t):
    r'[\+\-]?[0-9]+'
    return Integer(t.value)

## symbol token
def t_symbol(t):
    r'[a-zA-Z0-9_\?\:\;\+\-\*\/\.]+'
    return Symbol(t.value)

## lexer error callback
def t_error(t):
    raise SyntaxError(t)

## lexer
lexer = lex.lex()

## @}

## @defgroup repl REPL
## @brief Read-Eval-Print-Loop
## @{

## parse single word from source stream
## @returns `false` if end of source found
## @returns parsed object on @ref stack and `true`
def WORD():
    global S
    token = lexer.token()
    if not token: return False  # end of source
    S.push(token) ; return True
    
## `FIND ( symbol -- callable|symbol )` search in vocabulary by name
def FIND():
    WN = S.pop()
    try:
        S.push(W[WN.value]) ; return True
    except KeyError:
        try:
            S.push(W[WN.value.upper()]) ; return True
        except KeyError:
            S.push(WN) ; return False

## execute callable object from stack
def EXECUTE(): S.pop()()
        
## process chunk of source code
## @param[in] SRC source code string
def INTERPRET(SRC):
    lexer.input(SRC)
    while True:
        if not WORD(): break
        if S.top().type in ['symbol']:
            if not FIND(): print '\nunknown',S.pop().head() ; break 
            EXECUTE()
        
## Read-Eval-Print-Loop
def REPL():
    while True:
        print S
        INTERPRET(raw_input('\n> '))

## @}

## @}

## @defgroup oop OOP
## @brief minimalistic object oriented programming
## 
## * full-sized languages like Smalltalk and Java has very complex object model
## * kbFORTH core built with objects in roots
## * class-based OOP models has a lot of limitations we don't want to have
##
## so we must provide very thin layer between kb core and user console
## * create objects of classes implemented in kb core
## * implement classless OOP model with 
## * late dispatch message passing 
##
## @{

## @}

## @defgroup web Web interface
## @brief Flask powered
## @{

## IP addr to bind 
IP = '0.0.0.0'

## IP port to bind
PORT = 8888

## debug mode must be enabled only on dev station
DEBUG = False

## @defgroup auth authorization
## @brief HTTPS and hashed login/password for single user only
## @{

## SSL modes:

## * `'adhoc'`
SSL = 'adhoc'

try:
    ## * self-signed `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`
    SSL = ('cert.pem', 'key.pem')
    # check files available
    for i in SSL: open(i+'x','r').close()
except IOError:
    ## * None: pure HTTP for Eclipse internal browser 
    SSL = None
    # force only local bind, does not put your ass to Internet or even LAN
    IP = '127.0.0.1'
    # enable debug on dev station
    DEBUG = True

## login hash (autorization for single user only)
LOGIN_HASH = ''
## password hash (autorization for single user only)
PSWD_HASH  = ''
# this module can't be publicated on github
from secrets import LOGIN_HASH, PSWD_HASH

from werkzeug.security import generate_password_hash,check_password_hash

## @}

import flask,flask_wtf,wtforms,flask_login

## Flask application
app = flask.Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY') or \
                            open('/etc/machine-id').readline()[:-1]

## login manager
logman = flask_login.LoginManager() ; logman.init_app(app)

## web user
class User(flask_login.UserMixin):
    ## construct user with given name
    ## @param[in] id unicode string
    def __init__(self,id):
        ## user id (unicode string)
        self.id = id

## login manager user laoder
## @ingroup auth
@logman.user_loader
def load_user(user_id):
    return User(user_id) 

## command entry web form
class CmdForm(flask_wtf.FlaskForm):
    ## error message
    error = wtforms.StringField('no error')
    ## FORTH code entry
    pad = wtforms.TextAreaField('padd',render_kw={'rows':7,'autocorrect':'off'})
    ## go button
    go  = wtforms.SubmitField('GO')


## @param[in] methods
@app.route('/', methods=['GET', 'POST'])
## `/` route
def index():
    if not flask_login.current_user.is_authenticated:
        return flask.redirect('/login')
    form = CmdForm()
    if form.validate_on_submit(): INTERPRET(form.pad.data)
    return flask.render_template('index.html',form=form,S=S,W=W)

## @brief login web form
## @ingroup auth
class LoginForm(flask_wtf.FlaskForm):
    ## login field
    login  = wtforms.StringField('login',render_kw={'autocomplete':'username'})
    ## password field (stared)
    pswd   = wtforms.PasswordField('password',render_kw={'autocomplete':'current_password'})
    ## submit button
    go = wtforms.SubmitField('GO')

## @param[in] methods
@app.route('/login', methods = ['GET', 'POST'])
## @brief `/login` route
## @ingroup auth
def login():
    # any try to relogin will kickout active user
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

## `/logout` route
## @ingroup auth
@app.route('/logout')
@flask_login.login_required
def logout():
    return flask.redirect('/login')

## @}

## @defgroup argv system startup
## @brief command line parsing and initialization
## @{

## process command line parameters
## @details
## * process list of files in command line and exit, or
## * run interactive console if no parameters given
def process_argv():
    if len(sys.argv) > 1:       # has command line parameters
        for i in sys.argv[1:]:
            F = open(i,'r') ; INTERPRET(F.read()) ; F.close()
    else:
#         REPL()
        app.run(debug=DEBUG,host=IP,port=PORT,ssl_context=SSL)
process_argv()

## @}

