# https://www.youtube.com/playlist?list=PLddc343N7YqgYvD0Kfc91QUcssH_5_sn8

import os,sys,time,re,pickle

class Object:
    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.value = V
        self.attr = {}
        self.nest = []
    def __setitem__(self,key,obj):
        self.attr[key] = obj
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

class Container(Object): pass

class Stack(Object): pass

class Map(Container):
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

tokens = ['sym']

t_ignore = ' \t\r\n'

def t_sym(t):
    r'[0-9a-zA-Z_\.\?\+\-]+'
    return t

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()

def INTERPRET(SRC):
    lexer.input(SRC)
    while True:
        token = lexer.token()
        if not token: break
        print token

while True:
    print W,S
    try:
        INTERPRET(raw_input('\nbodik> '))
    except EOFError:
        BYE()
