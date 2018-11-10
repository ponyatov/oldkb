## @file
## @brief Symbolic Class system

## @defgroup sym Sym
## @brief Symbolic Frame/Class system
## @{

## @defgroup object Object
## @brief base object/frame class
## @{

class Object:

    ## constructor
    ## @param[in] V name / single primitive value 
    def __init__(self, V):
        ## type/class tag
        self.type  = self.__class__.__name__.lower()
        ## single primitive value from implementation language (Python/Java/..)
        self.value = V
        ## attr{}ibutes (*string-keyed associative*) <br>simulaneously:
        ## class slots, named stuct fields
        self.attr  = {}
        ## nest[]ed elements (*ordered*) <br>simulaneously:
        ## stack/vector/list
        self.nest  = []
        
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
    
    ## @defgroup dump print/dump
    ## @ingroup object
    ## @brief text representation for any object
    ## @{
        
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
    
    ## @}

## @}

## @}
 
