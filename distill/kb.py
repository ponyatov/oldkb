#!/usr/bin/env python2.7

## @file
## @brief engine

import os,sys,pickle,types

from Sym import * 

#     ## @ingroup msg
#     ## @{
#     
#     ## evaluate object in a generic recursive way
#     def eval(self):
#         for j in self.nest: j = j.eval()
#         return self
#     
#     def __call__(self): S.push(self) ; return self
#     
#     ## @}

# ## primitive object
# class Primitive(Object):
#     ## evaluate primitive as itself
#     ## @ingroup msg
#     def eval(self): return self

## @defgroup symbol symbol
## @brief names variables and other objects
## @{

# class Symbol(Primitive):
#     ## evaluate via vocabulary
#     ## @ingroup msg
#     def eval(self):
#         return self.lookup()
#     ## lookup in vocabulary 
#     ## @ingroup msg
#     def lookup(self):
#         try:
#             return W[self.value]
#         except KeyError:
#             try:
#                 return W[self.value.upper()]
#             except KeyError:
#                 raise KeyError(self)

## @defgroup nums numbers
## @brief multiple number classes: float, integer, complex...
## @{

## @defgroup math math
## @brief numerical computations starting from primitive arithmetics

import math

## floating pointer number
class Number(Primitive):
    ## @ingroup math
    ## @{
    
    def pfxadd(self): return Number(+self.value)
    def pfxsub(self): return Number(-self.value)
    
    def add(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(self.value + obj.value)
        raise SyntaxError(obj)
    
    def sub(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(self.value - obj.value)
        raise SyntaxError(obj)
    
    def mul(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(self.value * obj.value)
        raise SyntaxError(obj)
    
    def div(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(float(self.value) / obj.value)
        raise SyntaxError(obj)
    
    def pow(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(math.pow(self.value, obj.value))
        raise SyntaxError(obj)
    
    ## `( num -- sin(num) )` sinus
    def sin(self): return Number(math.sin(self.value))
    ## `( num -- cos(num) )` cosinus
    def cos(self): return Number(math.sin(self.value))
    ## `( num -- tan(num) )` tangens
    def tan(self): return Number(math.tan(self.value))
    ## @}
    
## integer number
class Integer(Number):
    ## @ingroup math
    ## @{
    
    def pfxadd(self): return Integer(+self.value)
    def pfxsub(self): return Integer(-self.value)
    
    def add(self,obj):
        if isinstance(obj, Integer): return Integer(self.value + obj.value)
        else: return Number.add(self,obj)
    def sub(self,obj):
        if isinstance(obj, Integer): return Integer(self.value - obj.value)
        else: return Number.sub(self,obj)
    def mul(self,obj):
        if isinstance(obj, Integer): return Integer(self.value * obj.value)
        else: return Number.mul(self,obj)
    def div(self,obj):
        return Number.div(self,obj)
    def pow(self,obj):
        if isinstance(obj, Integer): return Integer(math.pow(self.value, obj.value))
        else: return Number.add(self,obj)
    ## @}
        
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
    ## execute wrapped function
    ## @ingroup msg
    def __call__(self): self.fn()
    
## operator
class Op(Active):
    ## compute basic math operators
    ## @ingroup msg
    def eval(self):
        ## operator by its name
        if self.value == '~': return self.nest[0]
        if self.value == '+':
            if len(self.nest) == 1: return self.nest[0].eval().pfxadd()
            else: return self.nest[0].eval() .add( self.nest[1].eval() )
        if self.value == '-':
            if len(self.nest) == 1: return self.nest[0].eval().pfxsub()
            else: return self.nest[0].eval() .sub( self.nest[1].eval() )
        if self.value == '*':
            return self.nest[0].eval() .mul( self.nest[1].eval() )
        if self.value == '/':
            return self.nest[0].eval() .div( self.nest[1].eval() )
        if self.value == '^':
            return self.nest[0].eval() .pow( self.nest[1].eval() )
        return self

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

import ply.lex  as lex      # FORTH has no syntax we need lexer only
import ply.yacc as yacc     # tree script extension

## @defgroup lexer lexer
## @{

## token types list
## @details @ref sym
## * follows API of PLY library with object `type`/`value`
## * in result we able to directly use @ref prim s as tokens
## * and should use lowercased class names here
tokens = ['symbol','string','number','integer','hex','bin','eq','newline',
          'add','sub','mul','div','pow','lp','rp','tild']

## drop spaces
t_ignore = ' \t\r'

## line comments
def t_ignore_COMMENT(t):
    r'[#\\].*'

## count line number
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value) ; return t
    
## @defgroup brtokens bracket
## @brief `tokens`
## @{    
    
## `(`
def t_lp(t):
    r'\('
    return t
## `)`
def t_rp(t):
    r'\)'
    return t

## @}
    
## @defgroup optokens operator
## @brief `tokens`
## @{

## `+` token
def t_add(t):
    r'\+'
    t.value = Op(t.value) ; return t
## `-` token
def t_sub(t):
    r'\-'
    t.value = Op(t.value) ; return t
## `*` token
def t_mul(t):
    r'\*'
    t.value = Op(t.value) ; return t
## `/` token
def t_div(t):
    r'\/'
    t.value = Op(t.value) ; return t
## `^` token
def t_pow(t):
    r'\^'
    t.value = Op(t.value) ; return t

## `~` token
def t_tild(t):
    r'\~'
    t.value = Op(t.value) ; return t
    
## `=` eval operator
def t_eq(t):
    r'\='
    t.value = Symbol(t.value) ; return t
    
## @}

## @defgroup numtokens number
## @brief `tokens`
## @{
    
## hexadecimal
def t_hex(t):
    r'0x[0-9a-fA-F]+'
    t.value = Hex(t.value)
    t.type = t.value.type ; return t
    
## binary
def t_bin(t):
    r'0b[01]+'
    t.value = Bin(t.value)
    t.type = t.value.type ; return t
    
## exponential with integer base
def t_number_exp(t):
    r'[\+\-]?[0-9]+[eE][\+\-]?[0-9]+'
    t.value = Number(t.value)
    t.type = t.value.type ; return t
    
## floating point number token
def t_number(t):
    r'[\+\-]?[0-9]+\.[0-9]*([eE][\+\-]?[0-9]+)?'
    t.value = Number(t.value)
    t.type = t.value.type ; return t
    
## integer number token
def t_integer(t):
    r'[\+\-]?[0-9]+'
    t.value = Integer(t.value)
    t.type = t.value.type ; return t
    
## @}

## symbol token
def t_symbol(t):
    r'[a-zA-Z0-9_\?]+|[\.\:\;]'
    t.value = Symbol(t.value)
    t.type = t.value.type ; return t

## lexer error callback
## @ingroup plyerr
def t_error(t):
    raise SyntaxError(t)

## lexer
lexer = lex.lex()

## @}

## @defgroup parser parser
## @{

## operator precedence
precedence = (
    ('left','tild'),
    ('left','add','sub'),
    ('left','mul','div'),
    ('right','pow'),
    ('right','pfx'),
    )

## @defgroup plyrec recursive
## @brief REPL
## @{

## start of (empty) source
def p_none(p):
    ' tokens : '
    p[0] = []
    
## recursive end line separator
def p_recur_endline(p):
    ' tokens : tokens newline '
    p[0] = p[1]
    
## recursive rule for expressions
def p_recur_ex(p):
    ' tokens : tokens ex '
    p[0] = p[1] + [p[2]]
    
## send eval message to top object
def p_recur_eq(p):
    ' tokens : tokens eq '
    p[0] = p[1] + [p[2]]
    
## @}
    
## expression
def p_ex_primitive(p):
    ' ex : primitive '
    p[0] = p[1]
    
## @defgroup plyops operators
## @{

## `~A`    
def p_tild(p):
    ' ex : tild ex '
    p[0] = p[1] .push ( p[2] ) 
    
## `-A`
def p_add_pfx(p):
    ' ex : add ex %prec pfx'
    p[0] = p[1] .push( p[2] )
## `-A`    
def p_sub_pfx(p):
    ' ex : sub ex %prec pfx'
    p[0] = p[1] .push( p[2] )
    
## `A+B`
def p_add(p):
    ' ex : ex add ex '
    p[0] = p[2] .push ( p[1] ) .push ( p[3] )
## `A-B`
def p_sub(p):
    ' ex : ex sub ex '
    p[0] = p[2] .push ( p[1] ) .push ( p[3] )
## `A*B`
def p_mul(p):
    ' ex : ex mul ex '
    p[0] = p[2] .push ( p[1] ) .push ( p[3] )
## `A/B`
def p_div(p):
    ' ex : ex div ex '
    p[0] = p[2] .push ( p[1] ) .push ( p[3] )
## `A^B`
def p_pow(p):
    ' ex : ex pow ex '
    p[0] = p[2] .push ( p[1] ) .push ( p[3] )
    
## @}

## @defgroup plyparens parens
## @{

## `( )` parens
def p_ex_parens(p):
    ' ex : lp ex rp '
    p[0] = p[2]
    
## @}    

## primitive tokens
def p_primitive(p):
    ''' primitive : symbol
                  | number
                  | integer
                  | bin
                  | hex
                  | string    '''
    p[0] = p[1]
    
## parser error callback
## @ingroup plyerr
def p_error(p):
    raise SyntaxError(p)

## parser
parser = yacc.yacc(debug=False,write_tables=False)

## @}

## @defgroup plyerr error callbacks

## @defgroup parsegen iterator wrapper
## @{

## generator wrapper
def parser_generator(tokens):
    for i in tokens: yield i

## feed source code
def parser_feed(source):
    global parsed ; parsed = parser_generator(parser.parse(source))

## @}    

## @}

## @defgroup repl REPL
## @brief Read-Eval-Print-Loop
## @{

## parse single word from source stream
## @returns `false` if end of source found
## @returns parsed object on @ref stack and `true`
def WORD():
    global S
    #token = lexer.token()
    #if not token: return False  # end of source
    try:
        S.push( parsed.next() )
        return True
    except StopIteration:
        return False
    
## `FIND ( symbol -- callable|symbol )` search in vocabulary by name
def FIND():
    symbol = S.pop()
    try:
        S.push( symbol.lookup() ) ; return True
    except KeyError:
        S.push( symbol ) ; return False

## execute callable object from stack
## @ingroup msg
def EXECUTE(): S.pop()()

## `= ( obj -- obj.eval )` \ run eval message to top object
## @ingroup msg
def EQ(): S.push(S.pop().eval())
W['='] = Fn(EQ)

## @}


## process chunk of source code
## @param[in] SRC source code string
def INTERPRET(SRC):
    parser_feed(SRC)
    while True:
        if not WORD(): break
        if S.top().type in ['symbol']:
            if not FIND(): raise SyntaxError(S.pop())
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

## @defgroup msg Messaging

## @}

## @ingroup math
## @{

W['e'] = Number(math.e)
W['pi'] = Number(math.pi)

## sine
def SIN(): S.push ( S.pop().sin() )
## cosine
def COS(): S.push ( S.pop().cos() )
## tangens
def TAN(): S.push ( S.pop().tan() )

W << SIN ; W << COS ; W << TAN

## @}

## SSL modes:

## * None: pure HTTP for Eclipse internal browser 
SSL_KEYS = None
## * `'adhoc'`
SSL_KEYS = 'adhoc'
## * self-signed `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`
SSL_KEYS = ('cert.pem', 'key.pem')

## login hash (autorization for single user only)
LOGIN_HASH = ''
## password hash (autorization for single user only)
PSWD_HASH  = ''

from werkzeug.security import generate_password_hash,check_password_hash

## @}

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

## get/post
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
    login  = wtforms.StringField('login', [wtforms.validators.DataRequired()])
    ## password field (stared)
    pswd   = wtforms.PasswordField('password', [wtforms.validators.DataRequired()])
    ## submit button
    go = wtforms.SubmitField('GO')
    
## login
@app.route('/login', methods = ['GET', 'POST'])
## any try to relogin will kickout active user and invalidate all sessions
## @brief `/login` route
## @ingroup auth
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
#     app.config['SECRET_KEY'] = os.urandom(32)
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
        app.run(debug=DEBUG,host=IP,port=PORT,ssl_context=SSL_KEYS)
process_argv()

## @}

