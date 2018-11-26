#!/usr/bin/env python2.7

# metaLanguage engine: FORTH in Python -> ANSI'C

import os,sys

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

# stack
S = StacK('data')

# vocabulary
W = Map('FORTH')

W['S'] = S
W['W'] = W

def q(): print W
W['?'] = W['WORDS'] = Fn(q)

W['.'] = W['DROPALL'] = Fn(S.dropall)
W['DUP']   = Fn(S.dup)
W['DROP']  = Fn(S.drop)
W['SWAP']  = Fn(S.swap)
W['OVER']  = Fn(S.over)
W['PRESS'] = Fn(S.press)

def MODULE(): S.push( Module(S.pop().value) )
W << MODULE

def LSHIFT(): obj2 = S.pop() ; obj1 = S.pop() ; S.push( obj1 << obj2 )
W['<<'] = W['LSHIFT'] = Fn(LSHIFT)

import ply.lex as lex

tokens = ['sym','num','str']

t_ignore = ' \t\r\n'

def t_ignore_COMMENT(t):
    '\#.*'

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

try:
    with open(sys.argv[1],'r') as src: INTERPRET(src.read())
except IndexError:
    with open(sys.argv[0]+'.ml','r') as src: INTERPRET(src.read())
