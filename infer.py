## @file
## @brief back-tracking logic inference

## @defgroup infer Logic
## @brief back-tracking logic inference on trees/frames
## @details
## * [**YieldProlog**](http://yieldprolog.sourceforge.net/)
## * [Marvin Minky's Frame system](https://www.youtube.com/watch?v=nXJ_2uGWM-M&index=3&list=PLddc343N7YqgYvD0Kfc91QUcssH_5_sn8&t=24)
## * [Warren's Abstract Machine: A Tutorial Reconstruction](http://wambook.sourceforge.net/)
## * [CS164: Logic Programming Languages and Compilers](https://www.youtube.com/playlist?list=PLddc343N7YqgYvD0Kfc91QUcssH_5_sn8)
##   * Lec.5 [Coroutines & Yield](https://www.youtube.com/watch?v=chJQC_3WUqg&index=9&list=PLddc343N7YqgYvD0Kfc91QUcssH_5_sn8)
##     Python already has `yield` implemented
##   * Lec.6 [Intro to Prolog](https://www.youtube.com/watch?v=NT5RiJ6tgv8&list=PLddc343N7YqgYvD0Kfc91QUcssH_5_sn8&index=9)
##     **look it first**
##     * [SWI Prolog online](https://swish.swi-prolog.org/) for test and learning
##     * [look here first](https://swish.swi-prolog.org/p/CS_164_Prolog_intro_implementing.swinb)
##       notebook with sample code and links for SWI Prolog (reference system)
##   * **Lec.7** [**real magic starts here**](https://www.youtube.com/watch?v=HKUL_iLYTQs&list=PLddc343N7YqgYvD0Kfc91QUcssH_5_sn8&index=11)
## * Simpsons Prolog
##   * https://threefiddyblog.wordpress.com/2017/06/25/prolog-logical-programming-and-the-simpsons/
 
## @{

# yield with 
## unifying logic variable
class Var:
    def __init__(self,init=None): self.value = init
    def __repr__(self):
        
        if self.value: R = str(self.value)
        else: R=''
        return '<%s> @%X' % (R,id(self))
    ## `<<` unifying operator
    def __lshift__(self,arg): return self.unify(arg)
    def unify(self,arg):
        if not self.value:      # == if not bound
            self.value = arg    # bind
            yield self          # return self bounded
            self.value = None   # remove binding
        elif self.value == arg: # == or bounded var is equals
            yield self          # return self unmodified

def generalGetValue(arg):
    if isinstance(arg,Var):
        if not arg.value: return arg        # unbound var as itself
        else: return arg.value              # bound var.value
    else: return arg                        # other objects as is

def generalUnify(arg1, arg2, debug=False):
    if debug: print generalUnify
    if debug: print 'args',arg1,arg2
    arg1val = generalGetValue(arg1)
    arg2val = generalGetValue(arg2)
    if debug: print 'vals',arg1val,arg2val
    if isinstance(arg1val, Var):            # unbound arg1
        for i in arg1val << arg2val:
            yield i
    elif isinstance(arg2val, Var):          # unbound arg2
        for j in arg2val << arg1val:
            yield j
    else:                                   # both arg1/2 not Vars
        if arg1val == arg2val:
            yield Var(arg1val)
    if debug: print 
    
for i in generalUnify( Var(), Var(2) ): print i
for i in generalUnify(     2, Var()  ): print i
for i in generalUnify( Var(), Var()  ): print i
for i in generalUnify(     1, 1      ): print i

def male(P):
    for i in 'Homer Bart Abraham Skinner'.split():
        for j in generalUnify(P,i):
            yield j

def female(P):
    for i in 'Marge Lisa Maggie Paty Selma Mona Jacqueline'.split():
        for j in generalUnify(P,i):
            yield j
            
P = Var() #; P.value = 'Marge'; 
print 'P',P,
print ; print
for i in male(P): print i,
print ; print
for j in female(P): print j,
print ; print

def brother(Person, Brother):
    for i in generalUnify(Brother, 'Bart'):
        for j in generalUnify(Person, 'Lisa'):  yield i,'is brother',j
        for j in generalUnify(Person, 'Marge'): yield i,'is brother',j
    
for b in brother(Var(),'Bart'): print b

## @}
