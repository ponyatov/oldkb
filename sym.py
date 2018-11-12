
import os,sys,time,pickle

class Object:
    def __init__(self, V):
        self.type  = self.__class__.__name__.lower()
        self.value = V
        self.attr  = {}
        self.nest  = []
        
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
    
    def __setitem__(self,key,obj): self.attr[key] = obj ; return self
    def __getitem__(self,key): return self.attr[key]
    def __lshift__(self,obj): self.attr[obj.value] = obj

    def push(self,obj): self.nest.append(obj) ; return self
    def pop(self): return self.nest.pop()
    def top(self): return self.nest[-1]
    def dropall(self): self.nest = []
    
    def dup(self): self.push(self.top())
    def drop(self): self.pop()
    def swap(self): B = self.pop() ; A = self.pop() ; self.push(B) ; self.push(A)
    def over(self): self.push(self.nest[-2])
    
class Primitite(Object): pass
class Symbol(Primitite): pass
class String(Primitite): pass

class Number(Primitite):
    def __init__(self,V): Primitive.__init__(self, float(V))
class Integer(Number):
    def __init__(self,V): Primitive.__init__(self, int(V))

class Container(Object): pass
class Stack(Container): pass
class Map(Container): pass

class Active(Object): pass
class VM(Active): pass
class Fn(Active):
    def __init__(self,F): Active.__init__(self, F.__name__) ; self.fn = F
    def __call__(self,vm): self.fn(vm)
