## @file
## @brief Object/Frame FORTH-like system

## @defgroup forth FORTH
## @brief object/frame FORTH-like system
## @{

import os,sys,time,pickle

from Sym import *

class Class(Object): pass    
class Frame(Object): pass

################################### data containers ###########################
class Container(Object): pass
class Stack(Container): pass
class Map(Container): pass

############################## objects has executable semantics ###############
class Active(Object): pass
class VM(Active): pass
class Fn(Active):
    def __init__(self,F): Active.__init__(self, F.__name__) ; self.fn = F
    def __call__(self,vm): self.fn(vm)
    
################################## FORTH machine as CLI #######################    

## @defgroup ffvm VM
## @{

## global virtual machine
F = VM('FORTH')

F['vm'] = F

## @}

def BYE(vm): sys.exit(0)
F << Fn(BYE)

def q(vm): print vm.pop()
F['?'] = Fn(q)

###################################### classical stack banging ###############

def DUP(vm): vm.dup()
F << Fn(DUP)

def DROP(vm): vm.drop()
F << Fn(DROP)

def SWAP(vm): vm.swap()
F << Fn(SWAP)

def OVER(vm): vm.over()
F << Fn(OVER)

def DROPALL(vm): vm.dropall()
F << Fn(DROPALL)
F['.'] = Fn(DROPALL)

################################### frame manipuations ########################

def ST(vm):
    obj = vm.pop() ; slot = vm.pop() ; vm.top()[slot.value] = obj
F << Fn(ST)
F['!'] = Fn(ST)

def LD(vm):
    slot = vm.pop()
    try: vm.push ( vm.top()[slot.value] )
    except KeyError: vm.push( slot )
F << Fn(LD)
F['@'] = Fn(LD)

def SUB(vm):
    obj = vm.pop() ; vm.top() << obj
F << Fn(SUB)
F['//'] = Fn(SUB)

def PUSH(vm):
    obj = vm.pop() ; vm.top().push(obj)
F << Fn(PUSH)
F['<<'] = Fn(PUSH)

def pDROP(vm):
    vm.top().drop()
F['.DROP'] = Fn(pDROP)

##################################### parser ################################## 

import ply.lex as lex

tokens = ['symbol']

t_ignore = ' \t\r\n'

def t_symbol(t):
    r'[a-zA-Z0-9_\?\.\:\;\+\-\*\/\^\@\!\<\>]+'
    return Symbol(t.value)

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()

###################################### interpreter ############################

def WORD(vm):
    token = lexer.token()
    if not token: return False
    vm.push( token ) ; return True
F << Fn(WORD)
    
def FIND(vm):
    token = vm.pop()
    try: vm.push( vm[token.value] ) ; return True
    except KeyError:
        try: vm.push( vm[token.value.upper()] ) ; return True
        except KeyError:       vm.push( token ) ; return False
F << Fn(FIND)
    
def EXECUTE(vm):
    if callable(vm.top()): vm.pop() (vm)
F << Fn(EXECUTE)

def INTERPRET(vm):
    lexer.input(vm.pop().value)
    while True:
        if not WORD(vm): break
        if isinstance(vm.top(),Symbol):
            if FIND(vm): EXECUTE(vm)
F << Fn(INTERPRET)

################################### system startup ############################

while __name__ == '__main__':
    print F.dump(slots=None)
    F.push( String( raw_input('\ninfer> ') ) ) ; INTERPRET(F)

## @}
