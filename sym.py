
import os,sys,time,pickle

################################# Object #####################################

class Object:
    def __init__(self, V):
        self.type  = self.__class__.__name__.lower()
        self.value = V
        self.attr  = {}
        self.nest  = []
        
    ############## dump ##############
        
    def __repr__(self): return self.dump()
    dumped = []
    def dump(self, depth=0, prefix='', slots=True):
        S = self.pad(depth) + self.head(prefix)
        if not depth: Object.dumped = []
        if self in Object.dumped: return S + '...' 
        else: Object.dumped.append(self)
        if slots:
            for i in self.attr: S += self.attr[i].dump(depth + 1, prefix = '%s = ' % i)
        for j in self.nest: S += j.dump(depth + 1)
        return S
    def head(self, prefix=''):
        return '%s<%s:%s> @%x' % (prefix, self.type, self.str(), id(self))
    def pad(self, N): return '\n' + '    ' * N
    def str(self): return str(self.value)
    
    ############## slots ##############
        
    def __setitem__(self,key,obj): self.attr[key] = obj ; return self
    def __getitem__(self,key): return self.attr[key]
    def __lshift__(self,obj): self.attr[obj.value] = obj

    ############## stack ##############
        
    def push(self,obj): self.nest.append(obj) ; return self
    def pop(self): return self.nest.pop()
    def top(self): return self.nest[-1]
    def dropall(self): self.nest = []
    
    def dup(self): self.push(self.top())
    def drop(self): self.pop()
    def swap(self): B = self.pop() ; A = self.pop() ; self.push(B) ; self.push(A)
    def over(self): self.push(self.nest[-2])
    
################################### Primitive #################################   

class Primitive(Object): pass
class Symbol(Primitive): pass
class String(Primitive): pass

#################################### Number ###################################

import math

class Number(Primitive):
    def __init__(self,V): Primitive.__init__(self, float(V))

    def pfxadd(self): return self.__class__(+self.value)
    def pfxsub(self): return self.__class__(-self.value)
    
    def add(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(self.value + obj.value)
        raise SyntaxError(obj)
    def sub(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(self.value - obj.value)
        raise SyntaxError(obj)
    def mul(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(self.value * obj.value)
        raise SyntaxError(obj)
    def div(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(self.value / obj.value)
        raise SyntaxError(obj)
    
    def int(self): return Integer(self.value)
    def num(self): return self
    
################################### Integer ###################################

class Integer(Number):
    def __init__(self,V): Primitive.__init__(self, int(V))
    
    def add(self,obj):
        if isinstance(obj, Integer):
            return Integer(self.value + obj.value)
        if isinstance(obj, Number):
            return Number(float(self.value) + obj.value)
        raise SyntaxError(obj)
    def sub(self,obj):
        if isinstance(obj, Integer):
            return Integer(self.value - obj.value)
        if isinstance(obj, Number):
            return Number(float(self.value) - obj.value)
        raise SyntaxError(obj)
    def mul(self,obj):
        if isinstance(obj, Integer):
            return Integer(self.value * obj.value)
        if isinstance(obj, Number):
            return Number(float(self.value) * obj.value)
        raise SyntaxError(obj)
    def div(self,obj):
        if isinstance(obj, (Integer,Number)):
            return Number(float(self.value) / obj.value)
        raise SyntaxError(obj)
    
    def int(self): return self
    def num(self): return Number(self.value)

class Hex(Integer): 
    def __init__(self,V): Primitive.__init__(self, int(V[2:],0x10))
    def str(self): return '0x%X' % self.value
class Bin(Integer): 
    def __init__(self,V): Primitive.__init__(self, int(V[2:],0x02))
    def str(self): return bin(self.value)
    
################################### Container #################################

class Container(Object): pass
class Stack(Container): pass
class Map(Container): pass

#################################### Active ###################################

class Active(Object): pass
class VM(Active): pass
class Fn(Active):
    def __init__(self,F): Active.__init__(self, F.__name__) ; self.fn = F
    def __call__(self,vm): self.fn(vm)
