# Lisp in Small Pieces
# [ru] https://habr.com/post/204442/
#      http://blog.ilammy.net/lisp/

import os,sys

print sys.argv

class Atom:
    def __init__(self,V): self.value = V
    def __repr__(self): return '<%s>' % self.value
        
class Number(Atom): pass

class Cons:
    def __init__(self,A,D): self.A = A ; self.D = D
    def __repr__(self):

## @brief `eval`
## @param[in] exp expression to be evaluated
## @param env environment with bound variables
## @returns evaluated result
def evaluate(exp,env=[]):
    if isinstance(exp, Atom): return exp        # atoms evaluates to itself
    raise TypeError(exp)

print evaluate(Number(1.1))
print evaluate(Atom(None))
print evaluate([])
