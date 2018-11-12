# yLisp machine
# https://ponyatov.quora.com/%C2%B5Lisp-in-Python

def quote(args): return args

def apply(args): return args[0] ( args[1] )

def map(args): return [ args[0](i) for i in args[1] ]

# the Lisp magic
def eval(that):
    # evaluate atoms as is
    if not isinstance(that,(list,tuple)): return that
    # the first element of a list is a processing function
    fn   = eval( that[0] )
    # other elements are optional arguments
    if fn != quote: args = [ eval(item) for item in that[1:] ]
    # quote blocks the evaluation
    else:           args = that[1:]
    return fn(args)

def plus(args): return sum(args)

def inc(arg): return arg+1

print eval([plus,1,2,3])
print eval((plus,1,2,3))
print eval((plus, 3, (plus, 2, 10), 5))

print eval([quote,1,2,3])

print eval([quote,1,[quote,2,3]])

# print eval((plus, (quote, 1, 2, 3)))
print eval((apply, plus, (quote, 1, 2, 3)))

print eval((map, inc, (quote, 1, 2, 3)))
