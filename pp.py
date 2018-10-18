## @file
## @brief engine

import os,sys,pickle

## @defgroup sym symbolic class system

## base object
class Object:
    ## constructor 
    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.value = V
    ## print/dump
    def __repr__(self):
        return self.dump()
    def dump(self,depth=0):
        S = self.pad(depth) + self.head()
        return S
    def head(self,prefix=''):
        return '%s<%s:%s> @%X' % (prefix, self.type, self.value, id(self))
    def pad(self,N):
        return '\n'+'\t'*N

## primitives

class Primitive(Object): pass

class Symbol(Primitive): pass

class Number(Primitive): pass

class Integer(Number): pass

class String(Object): pass

## data containers

class Container(Object): pass

class Stack(Container): pass

class Map(Container): pass

class Vector(Container): pass

## active elements has execution semantics

class Active(Object): pass

class VM(Active): pass

########## FORTH VM

S = Stack('DATA')

W = Map('FORTH')

def LOAD():
    global W
    try: F = open(sys.argv[0]+'.db','r') ; W = pickle.load(F) ; F.close()
    except: pass
LOAD()

def SAVE():
    global W
    F = open(sys.argv[0]+'.db','w') ; pickle.dump(W, F) ; F.close()
SAVE()

def qq():
    print W ; print S

qq()
