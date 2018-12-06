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
def q(vm): print vm.dump(slots=False)
F['?'] = Cmd(q)

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
F['.'] = Cmd(DROPALL)

## @}

# ################################# math #####################################
## @ingroup math
## @{

## `+ ADD ( a b -- a+b )`
def ADD(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.add(B))
F << ADD
F['+'] = Cmd(ADD)

## `- SUB ( a b -- a-b )`
def SUB(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.sub(B))
F << SUB
F['-'] = Cmd(SUB)

## `* MUL ( a b -- a*b )`
def MUL(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.mul(B))
F << MUL
F['*'] = Cmd(MUL)

## `/ DIV ( a b -- a/b )`
def DIV(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.div(B))
F << DIV
F['/'] = Cmd(DIV)

## `% MOD ( a b -- a%b )`
def MOD(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.mod(B))
F << MOD
F['%'] = Cmd(MOD)

## `^ POW ( a b -- a^b )`
def POW(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.pow(B))
F << POW
F['^'] = Cmd(POW)

## `SQRT ( a -- Va )` square root
def SQRT(vm): vm.push(vm.pop().sqrt())
F << SQRT

## `SIN ( a -- sin(a) )`
def SIN(vm): vm.push(vm.pop().sin())
F << SIN

## `COS ( a -- cos(a) )`
def COS(vm): vm.push(vm.pop().cos())
F << COS

## `TAN ( a -- tan(a) )`
def TAN(vm): vm.push(vm.pop().tan())
F << TAN

## `INT ( number: -- integer: )` trail to integer part
def INT(vm): vm.push(vm.pop().int())
F << INT

## `NUM ( integer: -- number: )` to floating point
def NUM(vm): vm.push(vm.pop().num())
F << NUM

F['E']  = Number(math.e)
F['PI'] = Number(math.pi)

## @}

# ############################### interpreter ################################
## @defgroup interpret Interpreter
## @brief Simplest postfix script language
## @{

from syntax import *

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

# ####################### container manipulations ############################
## @ingroup cont
## @{

## `VECTOR ( symbol:name -- vector:name )`  create vector
def VECTOR(vm):
    vm.push(Vector(vm.pop().value))
F << VECTOR

## `STACK ( symbol:name -- stack:name )` create stack
def STACK(vm):
    vm.push(Stack(vm.pop().value))
F << STACK

## `MAP ( symbol:name -- map:name )` create associative array
def MAP(vm):
    vm.push(Map(vm.pop().value))
F << MAP

## @}

# ############################ Documenting ###############################
## @ingroup doc Documenting
## @{

def URL(vm): vm.push(Url(vm.pop().value))
F << URL

## @}

# ############################### messaging ##################################
## @ingroup persist
## @{

## `.SAVE ( obj -- obj )` save object to persistant store
def pSAVE(vm): vm.top().save()
F['.SAVE'] = Cmd(pSAVE)

## `.LOAD ( obj -- obj )` load object from persistant store
def pLOAD(vm): vm.top().load()
F['.LOAD'] = Cmd(pLOAD)

## @}

## @defgroup compose compose
## @ingroup msg
## @brief [de]compose objects inner/outer elements
## @{

## `// .PUSH ( obj1 obj2 -- obj1/obj2 )` push obj2 to obj1 (as stack)
def pPUSH(vm): obj2 = vm.pop() ; vm.top().push(obj2)
F['.PUSH'] = Cmd(pPUSH)
F['//']    = Cmd(pPUSH)

## `.POP ( obj1/obj2 -- obj1 obj2 )` decompose obj1 by popping obj2
def pPOP(vm): vm.push(vm.top().pop())
F['.POP'] = Cmd(pPOP)

## `.DROP ( obj1/obj2 -- obj1 )` drop from obj1
def pDROP(vm): vm.top().drop()
F['.DROP'] = Cmd(pDROP)

## `.FETCH @ ( obj1 name -- obj2 )` fetch slot from obj1 by name
def pFETCH(vm): name = vm.pop() ; obj1 = vm.pop() ; vm.push(obj1[name.value])
F['.FETCH'] = Cmd(pFETCH)
F['@'] = Cmd(pFETCH)

## `.STORE ! ( obj1 obj2 name -- obj1.name=obj2 )` store obj2 to obj1 slot with name
def pSTORE(vm): name = vm.pop() ; obj2 = vm.pop() ; vm.top()[name.value] = obj2
F['.STORE'] = Cmd(pSTORE)
F['!'] = Cmd(pSTORE)

## `.SLOT ( obj1 obj2 -- obj1.obj2 )` push obj2 as slot into obj1
def pSLOT(vm): obj2 = vm.pop() ; vm.top() << obj2
F['.SLOT'] = Cmd(pSLOT)    
F['$'] = Cmd(pSLOT)    

## `.DEL ( obj.key key -- obj )` delete object by key
def pDEL(vm): key = vm.pop().value ; vm.top().delete(key)
F['.DEL'] = Cmd(pDEL)

## @}

# ############################ metaprogramming ###############################
## @ingroup meta
## @{

## `FN ( name -- fn:name )` define function
def FN(vm): vm.push(Fn(vm.pop().value))
F << FN

## `GROUP ( name -- group:name)` object group
def GROUP(vm): vm.push(Group(vm.pop().value))
F << GROUP

## `PRIV ( name -- priv:name)` private group
def PRIV(vm): vm.push(Priv(vm.pop().value))
F << PRIV

## @ingroup lang
## @{

## `LANG ( name -- lang:name )` programming language
def LANG(vm): vm.push(Lang(vm.pop().value))
F << LANG

## `SYNTAX ( name -- syntax:name )` syntax parser/checker
def SYNTAX(vm): vm.push(Syntax(vm.pop().value))
F << SYNTAX

## `COMPILER ( name -- compiler:name )` compiler/language implementation
def COMPILER(vm): vm.push(Compiler(vm.pop().value))
F << COMPILER

## @}

## @ingroup oop
## @{

## `INHER ( obj1 obj2 -- obj2.super=obj1 )` inherit obj2 from obj1
def INHER(vm):
    obj2 = vm.pop() ; obj1 = vm.pop()
    vm.push(obj2) ; obj2['super'] = obj1
F << INHER

## @}

## @ingroup hwsw
## @{

## `CPU ( name -- cpu:name)` define CPU
def CPU(vm): vm.push(Cpu(vm.pop().value))
F << CPU

## `MCU ( name -- mcu:name)` define MCU microcontroller SoC
def MCU(vm): vm.push(Mcu(vm.pop().value))
F << MCU

F << Mcu('STM32')

## `ARCH ( name -- arch:name)` define new architecture
def ARCH(vm): vm.push(Arch(vm.pop().value))
F << ARCH

F << Arch('x86')
F << Arch('arm')
F << Arch('mips')

## `OS ( name -- os:name )` define OS
def OS(vm): vm.push(Os(vm.pop().value))
F << OS

## @}

## @}

# ############################ PPS integration ###############################
## @ingroup pps
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
