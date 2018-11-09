
import os,sys,time,pickle

############################## base frame class ###############################
class Object:
    def __init__(self,V):
        self.type = self.__class__.__name__.lower() ; self.value = V
        self.attr = {} ; self.nest = []
        
    def __setitem__(self,key,obj): self.attr[key] = obj ; return self
    def __getitem__(self,key): return self.attr[key]
    def __lshift__(self,obj): self.attr[obj.value] = obj
        
    def push(self,obj): self.nest.append(obj) ; return self
    def pop(self): return self.nest.pop()
    def top(self): return self.nest[-1]
    def dropall(self): self.nest = []
    
    def dup(self): self.push(self.top())
    def drop(self): self.pop()
    def swap(self):
        B = self.pop() ; A = self.pop()
        self.push(B) ; self.push(A) 
    def over(self): self.push(self.nest[-2])
        
    def __repr__(self): return self.dump()
    dumped = []
    def dump(self,depth=0,prefix='',slots=True):
        S = self.pad(depth) + self.head(prefix)
        if not depth: Object.dumped=[]
        if self in Object.dumped: return S+'...' 
        else: Object.dumped.append(self)
        if slots:
            for i in self.attr: S += self.attr[i].dump(depth+1,prefix='%s = '%i)
            if self.nest: S += self.pad(depth+1) + '+'*22
        for j in self.nest: S += j.dump(depth+1)
        return S
    def head(self,prefix=''): return '%s<%s:%s>'%(prefix,self.type,self.value)
    def pad(self,N): return '\n'+'    '*N

class Class(Object): pass    
class Frame(Object): pass

################################# primitives ##################################
class Primitite(Object): pass
class Symbol(Primitite): pass
class Number(Primitite): pass
class String(Primitite): pass

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

F = VM('FORTH')

F['vm'] = F

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
