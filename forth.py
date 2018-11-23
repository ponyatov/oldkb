## @file
## @ref kbf FORTH-like script language

## @defgroup forth kb/FORTH
## @brief @ref FORTH-like script language (more: @ref kbf)
## @{ 

from sym import *

# ############################# FORTH Virtual Machine ########################

## @ref kbf Virtual Machine
class FORTH(VM): pass

## global FVM
F = FORTH('vm')

F['VM'] = F

# ################################## debug ###################################
## @ingroup debug
## @{

## `BYE ( -- )` stop whole system
def BYE(vm): sys.exit(0)
F << BYE

## `? ( -- )` dump stack
def q(vm): print vm.pop()
F['?'] = Fn(q)

## `WORDS ( -- slots )` isolate vocabulary
def WORDS(vm): vm.push(vm.slots())
F << WORDS

## @}

# ################################ persistance ###############################
## @ingroup persist
## @{

## `SAVE ( -- )` pickle VM to `.db` file
def SAVE(vm): vm.save()
F << SAVE

## `LOAD ( -- )` unpickle VM from `.db` file
def LOAD(vm): vm.load()
F << LOAD

## @}

# ################################## stack ###################################
## @ingroup stack
## @{

## `DUP ( obj -- obj obj )`
def DUP(vm): vm.dup()
F << DUP

## `DROP ( obj1 obj2 -- obj1 )`
def DROP(vm): vm.drop()
F << DROP

## `SWAP ( obj1 obj2 -- obj2 obj1 )`
def SWAP(vm): vm.swap()
F << SWAP

## `OVER ( obj1 obj2 -- obj1 obj2 obj1 )`
def OVER(vm): vm.over()
F << OVER

## `PRESS ( obj1 obj2 -- obj2 )`
def PRESS(vm): vm.press()
F << PRESS

## `DROPALL ( `...` -- )` clear stack
def DROPALL(vm): vm.dropall()
F << DROPALL
F['.'] = Fn(DROPALL)

## @}

# ################################# math #####################################
## @ingroup math
## @{

## `+ ADD ( a b -- a+b )`
def ADD(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.add(B))
F << ADD
F['+'] = Fn(ADD)

## `- SUB ( a b -- a-b )`
def SUB(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.sub(B))
F << SUB
F['-'] = Fn(SUB)

## `* MUL ( a b -- a*b )`
def MUL(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.mul(B))
F << MUL
F['*'] = Fn(MUL)

## `/ DIV ( a b -- a/b )`
def DIV(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.div(B))
F << DIV
F['/'] = Fn(DIV)

## `% MOD ( a b -- a%b )`
def MOD(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.mod(B))
F << MOD
F['%'] = Fn(MOD)

## `^ POW ( a b -- a^b )`
def POW(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.pow(B))
F << POW
F['^'] = Fn(POW)

## `SQRT ( a -- Va )` square root
def SQRT(vm): vm.push(vm.pop().sqrt())
F << SQRT

## `sin ( a -- sin(a) )`
def SIN(vm): vm.push(vm.pop().sin())
F << SIN

## `cos ( a -- cos(a) )`
def COS(vm): vm.push(vm.pop().cos())
F << COS

## `tan ( a -- tan(a) )`
def TAN(vm): vm.push(vm.pop().tan())
F << TAN

## `int ( number: -- integer: )` trail to integer part
def INT(vm): vm.push(vm.pop().int())
F << INT

## `num ( integer: -- number: )` to floating point
def NUM(vm): vm.push(vm.pop().num())
F << NUM

F['E']  = Number(math.e)
F['PI'] = Number(math.pi)

## @}

# ############################### interpreter ################################
## @defgroup interpret Interpreter
## @brief Simplest postfix script language
## @{

from parser import *

## `WORD ( -- token )` read next token from source code stream
def WORD(vm):
    token = lexer.token()
    if not token: return False
    vm.push( token ) ; return True
F << WORD
    
## `FIND ( token -- callable | token )` lookup token in vocabulary
def FIND(vm):
    token = vm.pop()
    try: vm.push( vm[token.value] ) ; return True
    except KeyError:
        try: vm.push( vm[token.value.upper()] ) ; return True
        except KeyError:       vm.push( token ) ; return False
F << FIND
    
## `EXECUTE ( callable -- )` run executable object
def EXECUTE(vm):
    if callable(vm.top()): vm.pop() (vm)
F << EXECUTE

## `INTERPRET ( string:source -- )` interpret source code from string
def INTERPRET(vm):
    lexer.input(vm.pop().value)
    while True:
        if not WORD(vm): break
        if isinstance(vm.top(),Symbol):
            if FIND(vm): EXECUTE(vm)
F << INTERPRET

## @}

# ############################### messaging ##################################
## @defgroup msg messaging
## @brief message passing programming
## @{

## `.push ( obj1 obj2 -- obj1/obj2 )` push obj2 to obj1 (as stack)
def dPUSH(vm): obj2 = vm.pop() ; vm.top().push(obj2)
F['.PUSH'] = Fn(dPUSH)
F['//']    = Fn(dPUSH)

## `.pop ( obj1/obj2 -- obj1 obj2 )` decompose obj1 by popping obj2
def dPOP(vm): vm.push(vm.top().pop())
F['.POP'] = Fn(dPOP)

## `.save ( obj -- obj )` save object to persistant store
def pSAVE(vm): vm.top().save()
F['.SAVE'] = Fn(pSAVE)

## `.load ( obj -- obj )` load object from persistant store
def pLOAD(vm): vm.top().load()
F['.LOAD'] = Fn(pLOAD)

## @}

# ############################ PPS integration ###############################
## @defgroup ppsi PPS interface
## @{

from pps import *

F << Plan('plan')

## create new task
def TASK(vm): vm.push(Task(vm.pop().value))
F << TASK

## create big task (elephant)
def SLON(vm): vm.push(Slon(vm.pop().value))
F << SLON

## create boring task
def FROG(vm): vm.push(Frog(vm.pop().value))
F << FROG

## create new axis
def AXIS(vm): vm.push(Axis(vm.pop().value))
F << AXIS

## @}

# ################################# startup ##################################

while __name__ == '__main__':
    print F.dump(slots=None)
    F.push( String( raw_input('\ninfer> ') ) ) ; INTERPRET(F)

## @}
