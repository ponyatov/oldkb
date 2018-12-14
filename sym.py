## @file
## @brief Symbolic type system

## @defgroup sym Symbolic type system
## @brief universal object/frame/tree data structures
## @{ 

import os,sys,time,pickle

# ############################## Object #####################################
## @defgroup object Object 

## base generic *frame* object
## @ingroup object
class Object:
    ## construct generic *frame* object with given primitive `value`
    def __init__(self, V):
        ## type/class tag
        self.type  = self.__class__.__name__.lower()
        ## primitive value (implementation language type)
        self.value = V
        ## object attributes/slots
        self.attr  = {}
        ## nested elements = vector = stack
        self.nest  = []
        
    # ############# dump ##############
    ## @defgroup dump dump/print
    ## @brief represent object in human-readable text form
    ## @ingroup object
    ## @{
        
    ## print any object in a string form
    def __repr__(self): return self.dump()
    ## static list holds all objects dumped by last `dump()` method call
    dumped = []
    ## dump any object in tabbed tree text form
    def dump(self, depth=0, prefix='', slots=True, header=True):
        if header: S = self.pad(depth) + self.head(prefix)
        else: S = ''
        if not depth: Object.dumped = []
        if self in Object.dumped: return S + '...' 
        else: Object.dumped.append(self)
        if slots:
            for i in self.attr: S += self.attr[i].dump(depth + 1, prefix = '%s = ' % i)
        for j in self.nest: S += j.dump(depth + 1)
        if header: return S
        else: return S[1:]
    ## print only object `<type:value>` header
    def head(self, prefix=''):
        return '%s<%s:%s> @%x' % (prefix, self.type, self.str(), id(self))
    ## left pad with tabs
    def pad(self, N): return '\n' + '    ' * N
    ## convert value to string
    def str(self): return str(self.value)
    
    ## @}
    
    # ############# slots ##############
    ## @defgroup slot slot/attribute
    ## @brief operations on named attributes = frame slots
    ## @ingroup object
    ## @{

    ## `object[key] = value` operator
    ## @param[in] key string: slot name 
    def __setitem__(self,key,obj): self.attr[key] = obj ; return self
    ## `object[key]` operator
    ## @param[in] key string: slot name 
    def __getitem__(self,key): return self.attr[key]
    ## keys / slot names
    def keys(self): return self.attr.keys()
    ## `delete object[key]` operator
    ## @param[in] key string: slot name 
    def delete(self,key): del self.attr[key] ; return self
    ## `<<` operator: push `obj` as new slot
    ## @param [in] obj using `obj.value` as new slot name
    def __lshift__(self,obj):
        if isinstance(obj, Object): self.attr[obj.value] = obj
        elif callable(obj): self << Cmd(obj)
        else: raise TypeError(obj)
    ## operator `obj >> key` return inner `obj` slot
    ## @param[in] key string: slot name 
    def __rshift__(self,key):
        return self[key.value]
    ## print head `+ addr{}` names only
    def slots(self):
        R = self.head()+' :\n'
        for i in self.attr: R += '%s '%i
        return String(R)
    
    ## @}

    # ############# stack ##############
    ## @defgroup stack stack
    ## @brief Any object can act as generic stack
    ## @ingroup object
    ## @{
        
    ## push `obj` to `nest[]` as a stack
    def push(self,obj): self.nest.append(obj) ; return self
    ## pop top element from `nest[]`
    def pop(self): return self.nest.pop()
    ## get top `nest[]` stack element w/o removing it
    def top(self): return self.nest[-1]
    ## @brief `( ... -- )`
    def dropall(self): self.nest = []
    
    ## @brief `( obj -- obj obj )`
    def dup(self): self.push(self.top())
    ## @brief `( obj1 obj2 -- obj1 )`
    def drop(self): self.pop()
    ## @brief `( obj1 obj2 -- obj2 obj1)`
    def swap(self): B = self.pop() ; A = self.pop() ; self.push(B) ; self.push(A)
    ## @brief `( obj1 obj2 -- obj1 obj2 obj1 )`
    def over(self): self.push(self.nest[-2])
    ## @brief `( obj1 obj2 -- obj2 )`
    def press(self): del self.nest[-2]
    
    ## @}
    
    # ############## persistance ########
    ## @defgroup persist persistance
    ## @details @ref pp
    ## @ingroup object
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
        with open('db/%s/%s.obj'%(self.type,self.value) ,'w') as db:
            pickle.dump(self,db)
        
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

class String(Primitive):
    ## print strings with `\t\r\n` special chars in a single line
    def str(self):
        S = ''
        for c in self.value:
            if   c == '\t': S += '\\t'
            elif c == '\n': S += '\\n'
            else: S += c
        return S

# ################################ Number ###################################
## @defgroup num Number
## @brief Multiple number types (floating, integer, machine, complex,..)
## @{

## @defgroup math math
## @brief Basic numerical computations

import math

## floating point
class Number(Primitive):
    ## construct floating point number from string of number
    def __init__(self,V): Primitive.__init__(self, float(V))
    
    ## @ingroup math
    ## @{

    def pfxadd(self): return self.__class__(+self.value)
    def pfxsub(self): return self.__class__(-self.value)
    
    def add(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(self.value + obj.value)
        raise TypeError(obj)
    def sub(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(self.value - obj.value)
        raise TypeError(obj)
    def mul(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(self.value * obj.value)
        raise TypeError(obj)
    def div(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(self.value / obj.value)
        raise TypeError(obj)
    def pow(self,obj):
        if isinstance(obj, (Number,Integer)):
            return Number(math.pow(self.value, obj.value))
        raise TypeError(obj)

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
    ## construct integer number from string/number
    def __init__(self,V): Primitive.__init__(self, int(V))
    
    ## @ingroup math
    ## @{

    def add(self,obj):
        if isinstance(obj, Integer):
            return Integer(self.value + obj.value)
        if isinstance(obj, Number):
            return Number(float(self.value) + obj.value)
        raise TypeError(obj)
    def sub(self,obj):
        if isinstance(obj, Integer):
            return Integer(self.value - obj.value)
        if isinstance(obj, Number):
            return Number(float(self.value) - obj.value)
        raise TypeError(obj)
    def mul(self,obj):
        if isinstance(obj, Integer):
            return Integer(self.value * obj.value)
        if isinstance(obj, Number):
            return Number(float(self.value) * obj.value)
        raise TypeError(obj)
    def div(self,obj):
        if isinstance(obj, (Integer,Number)):
            return Number(float(self.value) / obj.value)
        raise TypeError(obj)
    def mod(self,obj):
        if isinstance(obj, Integer):
            return Integer(self.value % obj.value)
        raise TypeError(obj)
    def pow(self,obj):
        if isinstance(obj, Integer) and obj.value > 0:
            return Integer(math.pow(self.value, obj.value))
        elif isinstance(obj, (Integer,Number)):
            return Number(math.pow(self.value, obj.value))
        raise TypeError(obj)
    
    def int(self): return self
    def num(self): return Number(self.value)
    
    ## @}

## machine hexadecimal
class Hex(Integer):
    ## construct hex machine number from `0x` prefixed string
    def __init__(self,V): Primitive.__init__(self, int(V[2:],0x10))
    ## print with `0x` prefix
    def str(self): return '0x%X' % self.value
    
## binary string
class Bin(Integer): 
    ## construct binary string/number from `0b` prefixed string
    def __init__(self,V): Primitive.__init__(self, int(V[2:],0x02))
    ## print with `0b` prefix
    def str(self): return bin(self.value)
    
## @}
## @}
    
# ############################### Container #################################
## @defgroup cont Container
## @brief Data containers
## @{

class Container(Object): pass
class Vector(Container): pass
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

## VM command
class Cmd(Active):
    ## construct virtual machine command from Python function
    def __init__(self,F):
        Active.__init__(self, F.__name__)
        ## hold Python function pointer
        self.fn = F
    ## callable object
    def __call__(self,vm): self.fn(vm)
    
## @}

## @}

# ############################### Messaging ##################################
## @defgroup msg Messaging
## @brief message-passing OOP & distributed computing

# ############################ Documenting ###############################
## @defgroup doc Documenting
## @brief and html generation
## @{

class Doc(Object): pass

## @defgroup html HTML
## @brief HTML/CSS markup
## @{
class Html(Doc): pass
## @}

class Url(Doc): pass

class Email(Doc): pass

## @}

# ############################ Metaprogramming ###############################
## @defgroup meta Metaprogramming
## @{

class Meta(Object): pass

## object group
class Group(Meta): pass

## private group
class Priv(Group): pass

## @defgroup lang Syntax
## @brief Programming languages (parser/generate/compile)
## @{

## @brief programming language
class Lang(Meta): pass

## @brief syntax parser/checker
class Syntax(Lang): pass

## @brief compiler/language implementation
class Compiler(Lang): pass

## @}

# ################################ Generic ###################################
## @defgroup generic Generic
## @brief Generic (meta)programming using constructs common for most prog.languages
## @{

## @brief Generic metaprogramming
class Gen(Meta): pass

## @brief Function
class Fn(Gen): pass

## @brief Library
class Lib(Gen): pass

## @brief Module
class Module(Gen): pass

## @defgroup vcs VCS
## @brief Version Control System
## @{

## @brief Version Control System
class Vcs(Meta): pass
## @brief Git repo
class Git(Vcs): pass

## @}

## @defgroup emb Embedded
## @brief source code autogeneration for embedded systems
## @{

# ################################## LLVM ####################################
## @defgroup llvm LLVM
## @brief low-level code generation
    
# ################################# ANSI'C ###################################
## @defgroup c89 ANSI C'89
## @brief Portable code generation
## @{

## @brief ANSI'C
class C89(Lang): pass

## @}

## @}

## @defgroup webdev Web dev
## @{

## @defgroup py   Python
## @brief KB system bootstrap

## @defgroup go   Go
## @brief High-load backend

## @defgroup js   JavaScript
## @brief Frontend

## @}

## @defgroup cpp  C++
## @brief Native desktop 

## @defgroup java Java
## @brief Business hish-scale software development
## @{

## @defgroup android Android
## @brief Mobile

## @}

## @}

## @defgroup oop OOP

## @defgroup hwsw HWSW
## @brief hardware/software co-design
## @{

## hardware/software co-design metaobject
class HwSw(Meta): pass

## CPU processor/SoC
class Cpu(HwSw): pass
## MCU microcontroller
class Mcu(Cpu): pass

## ARCH computer architecture
class Arch(HwSw): pass

## OS operational system
class Os(HwSw): pass

## @defgroup stm32 STM32
## @brief [Cortex-M](https://ponyatov.quora.com/metaL-metaprogramming-for-STM32-Cortex-M-microcontrollers)
##        code generation target


## @}

# ######################### User Interface ##########################
## @defgroup ui UI
## @brief user interface
## @{

class UI(Meta): pass

## @}    

## @}
