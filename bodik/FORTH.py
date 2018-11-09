# object FORTH works over Marvin Minsky's frame model

import os,sys,time,re,pickle

# base generic unitree object = frame
# can act as any type wrapper, vector/stack, dict/map/vocabulary = slots

class Object:
    
    def __init__(self,V):
        # type/class tag, required for PLY parser library
        self.type  = self.__class__.__name__.lower()
        # signel value for primitive types from implementation language 
        self.value = V
        # slots = associative array keys
        self.attr  = {}
        # vector = stack = subtrees
        self.nest  = []

    # unitree operations 

    # frame[key] = obj            
    def __setitem__(self,key,obj):
        self.attr[key] = obj
    # frame << obj
    def __lshift__(self,obj):
        self.push(obj)
    def push(self,obj):
        self.nest.append(obj) ; return self
    
    # dumping
    
    def __repr__(self):
        return self.dump()
    dumped = []
    def dump(self,depth=0,prefix=''):
        S = self.pad(depth) + self.head(prefix)
        if not depth: Object.dumped = []
        if self in Object.dumped: return S + '...'
        Object.dumped.append(self)
        for i in self.attr:
            S += self.attr[i].dump(depth+1,prefix='%s = '%i)
        for j in self.nest:
            S += j.dump(depth+1)
        return S
    def head(self,prefix=''):
        return '%s<%s:%s>'%(prefix,self.type,self.value)
    def pad(self,N):
        return '\n'+'\t'*N
    
class Primitive(Object): pass

class Symbol(Primitive): pass

class Number(Primitive):
    def __init__(self,N):
        Primitive.__init__(self, float(N))

class Container(Object): pass

class Stack(Object): pass

class Map(Container):
    # map << obj
    def __lshift__(self,obj):
        if isinstance(obj,Object):
            self[obj.value] = obj
        elif callable(obj):
            self << Fn(obj)
        else:
            raise SyntaxError(obj)
        
class Active(Object): pass

class Fn(Active):
    def __init__(self,F):
        Active.__init__(self, F.__name__)
        self.fn = F

S = Stack('data')

W = Map('vocabulary')

W['W'] = W
W['S'] = S

def BYE(): sys.exit(0)
W << BYE

import ply.lex as lex

tokens = ['symbol','number']

t_ignore = ' \t\r\n'

def t_number(t):
    r'[\+\-]?[0-9]+(\.[0-9]*)?([eE][\+\-][0-9]+)?'
    return Number(t.value)
    
def t_symbol(t):
    r'[0-9a-zA-Z_\.\?\+\-]+'
    return Symbol(t.value)

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()

def INTERPRET(SRC):
    lexer.input(SRC)
    while True:
        token = lexer.token()
        if not token: break
        S << token

while True:
    print W,S
    try:
        INTERPRET(raw_input('\nbodik> '))
    except EOFError:
        BYE()
