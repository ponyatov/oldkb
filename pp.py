## @file
## @brief engine

import os,sys,pickle

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
        
    ## @defgroup dump print/dump
    ## @brief text representation for any object
    ## @{
    
    ## return text representation for any object
    def __repr__(self):
        return self.dump()
    ## dump in full tree form
    ## @param[in] depth tree padding
    def dump(self,depth=0):
        S = self.pad(depth) + self.head()
        return S
    ## dump in short header-only form
    def head(self,prefix=''):
        return '%s<%s:%s> @%X' % (prefix, self.type, self.value, id(self))
    ## left padding
    def pad(self,N):
        return '\n'+'\t'*N
    
    ## @}
    
    ## @defgroup symstack stack operations
    ## @ingroup stack
    ## @brief provided by Object
    ## @{
    
    ## @brief push nested object 
    def push(self,obj): self.nest.append(obj) ; return self
    ## @brief pop nested object
    def pop(self): return self.nest.pop()
    ## @}

## @defgroup prim primitive
## @brief close to machine level or implementation language types (Python)
## @{

class Primitive(Object): pass

class Symbol(Primitive): pass

class Number(Primitive): pass

class Integer(Number): pass

class String(Object): pass

## @}

## @defgroup cont data container
## @brief any object in @ref sym can be used as stack, vector and map
## @{

class Container(Object): pass

class Stack(Container): pass

class Map(Container): pass

class Vector(Container): pass

## @}

## @defgroup active active element
## @brief has execution semantics
## @{

class Active(Object): pass

class VM(Active): pass

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
LOAD()

## save vocabulary to pickle image
def SAVE():
    global W
    F = open(sys.argv[0]+'.db','w') ; pickle.dump(W, F) ; F.close()
SAVE()

## @}

## @defgroup deb debug
## @{

## `?? ( -- )` \ dump @ref fvm state
def qq():
    print W ; print S
    
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
tokens = ['symbol','number','integer','string']

## drop spaces
t_ignore = ' \t\r'

## line comments
def t_ignore_COMMENT(t):
    r'[#\\].*'

## count line number
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

## symbol token
def t_symbol(t):
    r'[a-zA-Z0-9_\?\:\;]+'
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
    token = lexer.token()
    if not token: return False  # end of source
    S.push(token) ; return True
    
## `FIND ( symbol -- callable )` search in vocabulary by name
def FIND():
    print S.pop()
    return False

## process chunk of source code
## @param[in] SRC source code string
def INTERPRET(SRC):
    lexer.input(SRC)
    while True:
        if not WORD(): break    # get next token
        if FIND(): EXECUTE()
        
## Read-Eval-Print-Loop
def REPL():
    while True:
        print S
        INTERPRET(raw_input('\n> '))

## @}

## @defgroup argv command line
## @brief parameters on system start
## @{

## process command line parameters
## @details
## * process list of files in command line and exit, or
## * run interactive console if no parameters given
def process_argv():
    if len(sys.argv) > 1:
        for i in sys.argv[1:]:
            F = open(i,'r') ; INTERPRET(F.read()) ; F.close()
    else:
        REPL()
process_argv()

## @}

## @}

