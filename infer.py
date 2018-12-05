## @file
## @brief back-tracking logic inferense

## @defgroup infer Logic
## @brief back-tracking logic inferense on trees/frames
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

## yield with logic variable'

class Var:
    def __init__(self): self.value = None
    def __lshift__(self,obj): self.value = obj ; return self
    def __repr__(self):
        if self.value: return '<%s>' % self.value
        else: return '<>'

def male(P):
    yield P << 'Homer'
    yield P << 'Bart'
    yield P << 'Abraham'
    yield P << 'Skinner'

def female(P):
    yield P << 'Marge'
    yield P << 'Lisa'
    yield P << 'Maggie'
    yield P << 'Mona'
    yield P << 'Jacqueline'
    yield P << 'Paty'
    yield P << 'Selma'

P = Var() ; print 'P',P,
print ; print
for i in male(P): print i,
print ; print
for j in female(P): print j,

## @}
