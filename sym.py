## @file
## @brief Symbolic type system

## @defgroup sym Symbolic type system
## @brief universal object/frame/tree data structures
## @{ 

import os,sys,time,pickle

# ############################## Object #####################################

class Object:
    def __init__(self, V):
        self.type  = self.__class__.__name__.lower()
        self.value = V
        self.attr  = {}
        self.nest  = []
        
    # ############# dump ##############
    ## @defgroup dump dump/print
    ## @brief represent object in human-readable text form
    ## @ingroup sym
    ## @{
        
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
    
    ## @}
    
    # ############# slots ##############
    ## @defgroup slot slot/attribute
    ## @brief operations on named attributes = frame slots
    ## @ingroup sym
    ## @{
        
    def __setitem__(self,key,obj): self.attr[key] = obj ; return self
    def __getitem__(self,key): return self.attr[key]
    def __lshift__(self,obj): self.attr[obj.value] = obj
    def slots(self):
        R = self.__class__(self.value)
        R.attr = self.attr
        return R
    
    ## @}

    # ############# stack ##############
    ## @defgroup stack stack
    ## @brief Any object can act as generic stack
    ## @ingroup sym
    ## @{
        
    def push(self,obj): self.nest.append(obj) ; return self
    def pop(self): return self.nest.pop()
    def top(self): return self.nest[-1]
    def dropall(self): self.nest = []
    
    def dup(self): self.push(self.top())
    def drop(self): self.pop()
    def swap(self): B = self.pop() ; A = self.pop() ; self.push(B) ; self.push(A)
    def over(self): self.push(self.nest[-2])
    
    ## @}
    
    # ############## persistance ########
    ## @defgroup persist persistance
    ## @details @ref pp
    ## @ingroup sym
    ## @{
    
    ## save to disk .db
    def save(self):
        try: os.mkdir('db')
        except OSError: pass
        try: os.mkdir('db/%s' % self.type)
        except OSError: pass
        with open('db/%s/%s.attr'%(self.type,self.value) ,'w') as db:
            pickle.dump(self.attr,db)
        with open('db/%s/%s.nest'%(self.type,self.value) ,'w') as db:
            pickle.dump(self.nest,db)
        
    ## restore from disk .db
    def load(self):
        try: os.mkdir('db')
        except OSError: pass
        try: os.mkdir('db/%s' % self.type)
        except OSError: pass
        with open('db/%s/%s.attr'%(self.type,self.value) ,'r') as db:
            self.attr = pickle.load(db)
        with open('db/%s/%s.nest'%(self.type,self.value) ,'r') as db:
            self.nest = pickle.load(db)
    
    ## @}

## @defgroup debug debug
    
# ############################### Primitive #################################
## @defgroup prim Primitive
## @brief primitive types in implementation language (Python)
## @{   

class Primitive(Object): pass
class Symbol(Primitive): pass
class String(Primitive): pass

# ################################ Number ###################################
## @defgroup num Number
## @brief Multiple number types (floating, integer, machine, complex,..)
## @{

## @defgroup math
## @brief Basic numerical computations

import math

## floating point
class Number(Primitive):
    def __init__(self,V): Primitive.__init__(self, float(V))
    
    ## @ingroup math
    ## @{

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
    def pow(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(math.pow(self.value, obj.value))
        raise SyntaxError(obj)

    def sqrt(self): return Number(math.sqrt(self.value))
    def sin(self):  return Number(math.sin(self.value))
    def cos(self):  return Number(math.cos(self.value))
    def tan(self):  return Number(math.tan(self.value))
    
    def int(self): return Integer(self.value)
    def num(self): return self
    
    ## @}
    
# ############################### Integer ###################################

## integer
class Integer(Number):
    def __init__(self,V): Primitive.__init__(self, int(V))
    
    ## @ingroup math
    ## @{

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
    def mod(self,obj):
        if isinstance(obj, Integer):
            return Integer(self.value % obj.value)
        raise SyntaxError(obj)
    def pow(self,obj):
        if isinstance(obj, Integer) and obj.value > 0:
            return Integer(math.pow(self.value, obj.value))
        elif isinstance(obj, (Integer,Number)):
            return Number(math.pow(self.value, obj.value))
        raise SyntaxError(obj)
    
    def int(self): return self
    def num(self): return Number(self.value)
    
    ## @}

## machine hexadecimal
class Hex(Integer): 
    def __init__(self,V): Primitive.__init__(self, int(V[2:],0x10))
    def str(self): return '0x%X' % self.value
    
## binary string
class Bin(Integer): 
    def __init__(self,V): Primitive.__init__(self, int(V[2:],0x02))
    def str(self): return bin(self.value)
    
## @}
## @}
    
# ############################### Container #################################
## @defgroup cont Container
## @brief Data containers
## @{

class Container(Object): pass
class Stack(Container): pass
class Map(Container): pass

## @}

# ################################ Active ###################################
## @defgroup active Active
## @brief Objects has execution semantics
## @{

class Active(Object): pass

## Virtual Machine
class VM(Active): pass

## Function
class Fn(Active):
    def __init__(self,F): Active.__init__(self, F.__name__) ; self.fn = F
    def __call__(self,vm): self.fn(vm)
    
## @}

## @}
