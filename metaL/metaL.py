#!/usr/bin/env python2.7

# metaLanguage engine: FORTH in Python -> ANSI'C

import os,sys

# ####################################################### symbolic type system

class Obj:
    # construct with name
    def __init__(self,V):
        self.type = self.__class__.__name__.lower() ; self.value = V
        self.attr = {} ; self.nest = []
        
    # print object
    def __repr__(self):
        return self.dump()
    dumped=[]
    def dump(self,depth=0,prefix=''):
        S = self.pad(depth) + self.head(prefix)
        if not depth: Obj.dumped = []
        if self in Obj.dumped: return S+'...'
        else: Obj.dumped.append(self)
        for i in self.attr: S += self.attr[i].dump(depth+1,prefix='%s = '%i)
        for j in self.nest: S += j.dump(depth+1)
        return S
    def head(self,prefix=''):
        return '%s<%s:%s>' % (prefix, self.type, self.value)
    def pad(self,N):
        return '\n' + '\t'*N

    # attr{}    
    def __setitem__(self,key,obj): self.attr[key] = obj ; return self
    def __getitem__(self,key): return self.attr[key]
    def __lshift__(self,obj):
        if isinstance(obj,Obj): self[obj.value] = obj ; return self
        if callable(obj): return self << Fn(obj)
        raise TypeError(obj)
    # nest[] as stack
    def dropall(self): self.nest = []
    def push(self,obj): self.nest.append(obj) ; return self
    def pop(self): return self.nest.pop()
    def top(self): return self.nest[-1]
    def dup(self): self.push(self.top())
    def drop(self): self.pop()
    def swap(self): B = self.pop() ; A = self.pop() ; self.push(B) ; self.push(A)
    def over(self): self.push(self.nest[-2])
    def press(self): del self.nest[-2]

    
class Sym(Obj): pass
class Str(Obj): pass
class Num(Obj): pass
class Int(Num): pass

class StacK(Obj): pass
class Map(Obj): pass

class Fn(Obj):
    def __init__(self,F): Obj.__init__(self, F.__name__) ; self.fn = F
    def __call__(self): self.fn()

class Module(Obj): pass

class Mcu(Obj): pass

# ############################################### virtual object FORTH machine

# stack
S = StacK('data')

# vocabulary
W = Map('FORTH')

W['S'] = S
W['W'] = W

def BYE(): sys.exit(0)
W << BYE

def q(): print S
W['?'] = W['WORDS'] = Fn(q)

def qq(): print W ; print S ; BYE()
W['??'] = Fn(qq)

# ################################################ target system configuration

def MCU(): W << Mcu(S.pop().value)
W << MCU

# ############################################################ metaprogramming

def MODULE(): S.push( Module(S.pop().value) )
W << MODULE

# ############################################################# stack swanking

W['.'] = W['DROPALL'] = Fn(S.dropall)
W['DUP']   = Fn(S.dup)
W['DROP']  = Fn(S.drop)
W['SWAP']  = Fn(S.swap)
W['OVER']  = Fn(S.over)
W['PRESS'] = Fn(S.press)

# FETCH @ ( name -- obj ) fetch obj from vocabulary by name
def FETCH(): S.push( W[S.pop().value] )
W << FETCH
W['@'] = Fn(FETCH)

# STORE ! ( obj name -- ) store obj to vocabulary with given name
def STORE(): name = S.pop().value ; W[name] = S.pop()
W << STORE
W['!'] = Fn(STORE)

# #################################################### structural manipulators

def LSHIFT(): obj2 = S.pop() ; obj1 = S.pop() ; S.push( obj1 << obj2 )
W['<<'] = W['LSHIFT'] = Fn(LSHIFT)

# ################################################# syntax parser (lexer only)

import ply.lex as lex

tokens = ['sym','num','str']

t_ignore = ' \t\r\n'

def t_ignore_COMMENT(t):
    '[\\\#].*'

states = (('str','exclusive'),)

t_str_ignore = ''

def t_str(t):
    r'\''
    t.lexer.string = '' ; t.lexer.push_state('str')
def t_str_str(t):
    r'\''
    t.lexer.pop_state() ; return Str(t.lexer.string)
def t_str_any(t):
    r'.'
    t.lexer.string += t.value

def t_num(t):
    r'[0-9]+'
    return Num(t.value)
def t_sym(t):
    r'[^ \t\r\n]+'
    return Sym(t.value)

def t_ANY_error(t): raise SyntaxError(t)

lexer = lex.lex()

# ########################################################## FORTH interpreter

def WORD():
    token = lexer.token()
    if not token: return False
    S.push(token) ; return True
W << WORD
    
def FIND():
    token = S.pop()
    try:
        S.push(W[token.value]) ; return True
    except KeyError:
        try: S.push(W[token.value.upper()]) ; return True
        except KeyError: S.push(token) ; return False
W << FIND
    
def EXECUTE():
    if callable(S.top()): S.pop() ()
W << EXECUTE
    
def INTERPRET(SRC):
    lexer.input(SRC)
    while True:
        if not WORD(): break
        if S.top().type in ['sym']:
            if FIND(): EXECUTE()
            else: raise KeyError(S.pop().head())

def REPL():
    while True: print S ; INTERPRET(raw_input('ok> '))
W << REPL

# #################################################################### compiler

def DEF(): WORD() ; STORE()
W << DEF

# ######################################################### object programming

def INHER():
    WORD() ; child = S.pop() ; super = S.pop()
    child.type = super.type ; child['super'] = super ; W << child
W << INHER

# ############################################################## system startup

for file in sys.argv[1:]:
    with open(file,'r') as src:
        INTERPRET(src.read())

if len(sys.argv) == 1: REPL()
