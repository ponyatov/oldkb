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
    r'[a-zA-Z0-9_\?\:\;\+\-\*\/]+'
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

## @defgroup web Web interface
## @brief Flask powered

## @{

## IP addr to bind
IP = '127.0.0.1'

## IP port to bind
PORT = 8888

import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html',S=S,W=W,PAD='\ kb/FORTH commands')

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
        app.run(debug=True,host=IP,port=PORT)
process_argv()

## @}

