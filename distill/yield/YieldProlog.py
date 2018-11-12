## @file
## @brief Yield Prolog

## @defgroup yp Yield Prolog 
## @brief <a href="http://yieldprolog.sourceforge.net/">Yield Prolog</a>
## variant on top of @ref sym
## @{

## @defgroup yprint object print
## @defgroup ynest nested elements

## logic term
class T:
    ## construct with name
    ## @param[in] V primitive value
    def __init__(self,V):
        ## primitive value
        self.value = V
        ## nested elements
        ## @ingroup ynest
        self.nest = []
    ## @ingroup yprint
    ## @{
    ## represent in string form
    def __repr__(self):
        return self.dump()
    ## full tree-like object dump
    ## @param[in] depth tree depth (recursive visitor)
    def dump(self,depth=0):
        S = self.pad(depth) + self.head()
        for j in self.nest: S += j.dump(depth+1)
        return S
    ## short dump: header only
    def head(self):
        return '<%s>' % self.value
    ## left pad with tabs for tree dump
    ## @param[in] N depth level
    def pad(self,N):
        return '\n' + '\t' * N
    ## @}
    ## push nested element
    ## @ingroup ynest
    def __lshift__(self,obj):
        self.nest.append(obj) ; return self
    ## iterate
    def __iter__(self): return iter(self.nest)
    ## iterate with unifing var
    def __call__(self,var):
        for i in self.nest: yield var % i

## @}

## @defgroup sample samples
## @ingroup yp
## @{ 

## sample object with 3 elements of diff.type
a = T('A') << T('B') << T(123) << T('C')

## unifing variable
class V(T):
    ## unification `%` operator
    def __mod__(self,obj):
        ## nested elements
        self.nest = [obj]
        return self

## test object
A = V('var')
for i in a(A): print i

## @}


