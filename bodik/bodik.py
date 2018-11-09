# https://www.youtube.com/playlist?list=PLddc343N7YqgYvD0Kfc91QUcssH_5_sn8

import os,sys,time,re,pickle

class Object:
    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.value = V
        self.attr = {}
        self.nest = []
    def __repr__(self):
        return self.dump()
    def dump(self,depth=0,prefix=''):
        S = self.pad(depth) + self.head(prefix)
        return S
    def head(self,prefix=''):
        return '%s<%s:%s>'%(prefix,self.type,self.value)
    def pad(self,N):
        return '\n'+'\t'*N

class Container(Object): pass

class Stack(Object): pass

class Map(Container): pass

def BYE(): sys.exit(0)

S = Stack('data')

W = Map('vocabulary')

import ply.lex as lex

tokens = ['sym']

t_ignore = ' \t\r\n'

def t_sym(t):
    r'[0-9a-zA-Z_\.\?\+\-]+'
    return t

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()

while True:
    print S.dump()+'\n'
    try:
        lexer.input(raw_input('bodik> '))
    except EOFError:
        BYE()
    while True:
        token = lexer.token()
        if not token: break
        print token
