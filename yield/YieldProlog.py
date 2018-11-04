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

## @}

## @defgroup sample samples
## @ingroup yp
## @{ 

## sample object with 3 elements of diff.type
A = T('A') << T('B') << T(123) << T('C') ; print A

## @}
