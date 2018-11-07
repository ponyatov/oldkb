# Lisp machine

def eval(that):
    # the magic
    if isinstance(that,(list,tuple)):
        # the first element of a list is a processing function
        fn   = eval( that[0] )
        # other elements are optional arguments
        args = [ eval(item) for item in that[1:] ]
        return fn(args)
    # evaluate atoms as is
    else: return that

def plus(args): return sum(args)

print eval([plus,1,2,3])
print eval((plus,1,2,3))
print eval((plus, 3, (plus, 2, 10), 5))