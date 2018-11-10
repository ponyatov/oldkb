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
    
    ## @defgroup symstack stack operations
    ## @ingroup object
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
    
    ## @defgroup print print/dump
    ## @ingroup object
    ## @brief text representation for any object
    ## @{
        
    ## text representation for any object (full tree dump)
    def __repr__(self): return self.dump()

    ## global dump registry to avoid infty dump 
    dumped = []

    ## dump any object in full tree form
    ## @param[in] depth tree padding
    ## @param[in] prefix prefix string before first line of subtree
    ## @param[in] slots flag to disable attr section dump (for @ref forth)
    def dump(self, depth=0, prefix='', slots=True):
        # left-padded header line
        S = self.pad(depth) + self.head(prefix)
        # block infinitive dump
        if not depth: Object.dumped = []
        if self in Object.dumped: return S + '...' 
        else: Object.dumped.append(self)
        # dump slots (default)
        if slots:
            for i in self.attr:
                S += self.attr[i].dump(depth + 1, prefix = '%s = ' % i)
        # dump nested elements
        for j in self.nest:
                S += j.dump(depth + 1)
        # return collected dump
        return S

    ## dump in short header-only form
    ## @param[in] prefix for attribute printing in dump() and plot()
    def head(self, prefix=''):
        return '%s<%s:%s> @%x' % (prefix, self.type, self.str(), id(self))

    ## string representation of value only w/o special formats
    def str(self): return str(self.value)
    
    ## left padding
    def pad(self, N): return '\n' + '    ' * N
    
    ## @}

## @}

## @}
 
