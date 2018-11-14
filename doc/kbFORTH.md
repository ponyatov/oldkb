# kb/FORTH {#kbf}

## @brief FORTH-like script language for frame/object/tree manipulations

FORTH is an old warm tube language extra simple in roots,
in fact has no syntax (lexer only), and very easy to implement.
So, it was selected as the first command line interface
for this knowledge base system prototype.

# concatenative programming language

http://en.wikipedia.org/wiki/Concatenative_programming_language

A concatenative programming language follows tacit/point-free programming 
paradigm, when function definitions do not identify the arguments (or "points") 
on which they operate. Instead the definitions should be composed from other 
functions, among which are combinators, that manipulate arguments on some 
shared data container structure (stack is mostly used). The lack of argument 
naming gives pointless style a reputation of being unnecessarily obscure, and 
FORTH has the same feel. The combination of a compositional semantics with a 
syntax that mirrors such a semantics makes concatenative languages highly a
menable to algebraic manipulation of programs (see Joy manual).

# FORTH was selected as a command language
## due to its simplicity in syntax and implementation

FORTH has a long history in this role from 1968, and it is indomitable as tiny 
CLI command shell:

* extra simple internals
* no syntax in fact (dumb lexer can be written in a few machine commands)
* require very small resources, can work in a few Kb of RAM and the same 
quantities of runtime code in ROM
* portability: you can rewrite working system from scratch in a weekend

But it has serious drawbacks kicks out FORTH from commercial development:

* no system protection: you can do errors on the stack, and data can be written 
in a random place in memory; OS will drop whole your program by segfault, and 
this the best case comparing to data corruption by unpredictable disk write or 
trash requests to DBMS
* low-level stack shaking: DUP SWAP smeared out all over the code, +1 step to 
code unreadability
* there is no fool protection in language: no type checking or memory protection 
barriers, you can write anything to any place in memory; as FORTH mainly 
targetted for an interactive session, this makes the system in common unstable 
and error-prone (it's the price of implementation simplicity)
* community dissipation due to creeping dialect nature: language itself is 
atomic, but you can get syntax wars even in a single tiny developing team due 
to preferences in the order of the parameters on the stack or string format 
(single object pointer in '84 vs addr/len pair in '94 standards)
* language primitivity together with the poverty of stdlib: you must reimplement 
from scratch everything available out of the shelf in other languages (
implementations)

To get the first feel, look into [Starting FORTH](http://www.forth.com/starting-forth/)
by Leo Brodie. This is good intro book available online for free. 
Don't dive too deep, we'll use some non-standard dialect based on objects 
(it can resemble Factor language). Just become friendly with 
concatenative programming using a stack and making simple definitions.

### appalling nonstandardity

**ANS'Forth diy**. Really, did you anytime see (not hear) about some software 
system written in Forth and still in use today? Standardization is good for 
efforts reuse, but it did not help Forth survive. And inside-outed IF was 
not engraved on stone tablets given as by the Godly Chuck. **The root idea of 
FORTH was `simplicity+flexibility`**. Chuck Moore itself jumped out into something 
alien-given like Color Forth...colorblinds were bewildered.

Dialects are bad for developers teams, it exfoliates community. Oops, are they exist, these teams?! Keep free if you can control it.