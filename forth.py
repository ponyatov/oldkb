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
F << Fn(BYE)

## `? ( -- )` dump stack
def q(vm): print vm.pop()
F['?'] = Fn(q)

## `WORDS ( -- )` dump vocabulary
def WORDS(vm): vm.push(vm.slots())
F << Fn(WORDS)

## @}

# ################################ persistance ###############################
## @ingroup persist
## @{

## `SAVE ( -- )` pickle VM to `.db` file
def SAVE(vm): vm.save()
F << Fn(SAVE)

## `LOAD ( -- )` unpickle VM from `.db` file
def LOAD(vm): vm.load()
F << Fn(LOAD)

## @}

# ################################## stack ###################################
## @ingroup stack
## @{

def DUP(vm): vm.dup()
F << Fn(DUP)

def DROP(vm): vm.drop()
F << Fn(DROP)

def SWAP(vm): vm.swap()
F << Fn(SWAP)

def OVER(vm): vm.over()
F << Fn(OVER)

def DROPALL(vm): vm.dropall()
F << Fn(DROPALL)
F['.'] = Fn(DROPALL)

## @}

# ################################# math #####################################
## @ingroup math
## @{

## `+ ADD ( a b -- a+b )`
def ADD(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.add(B))
F << Fn(ADD)
F['+'] = Fn(ADD)

## `- SUB ( a b -- a-b )`
def SUB(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.sub(B))
F << Fn(SUB)
F['-'] = Fn(SUB)

## `* MUL ( a b -- a*b )`
def MUL(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.mul(B))
F << Fn(MUL)
F['*'] = Fn(MUL)

## `/ DIV ( a b -- a/b )`
def DIV(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.div(B))
F << Fn(DIV)
F['/'] = Fn(DIV)

## `% MOD ( a b -- a%b )`
def MOD(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.mod(B))
F << Fn(MOD)
F['%'] = Fn(MOD)

## `^ POW ( a b -- a^b )`
def POW(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.pow(B))
F << Fn(POW)
F['^'] = Fn(POW)

## `SQRT ( a -- Va )` square root
def SQRT(vm): vm.push(vm.pop().sqrt())
F << Fn(SQRT)

## `sin ( a -- sin(a) )`
def SIN(vm): vm.push(vm.pop().sin())
F << Fn(SIN)

## `cos ( a -- cos(a) )`
def COS(vm): vm.push(vm.pop().cos())
F << Fn(COS)

## `tan ( a -- tan(a) )`
def TAN(vm): vm.push(vm.pop().tan())
F << Fn(TAN)

## `int ( number: -- integer: )` trail to integer part
def INT(vm): vm.push(vm.pop().int())
F << Fn(INT)

## `num ( integer: -- number: )` to floating point
def NUM(vm): vm.push(vm.pop().num())
F << Fn(NUM)

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
F << Fn(WORD)
    
## `FIND ( token -- callable | token )` lookup token in vocabulary
def FIND(vm):
    token = vm.pop()
    try: vm.push( vm[token.value] ) ; return True
    except KeyError:
        try: vm.push( vm[token.value.upper()] ) ; return True
        except KeyError:       vm.push( token ) ; return False
F << Fn(FIND)
    
## `EXECUTE ( callable -- )` run executable object
def EXECUTE(vm):
    if callable(vm.top()): vm.pop() (vm)
F << Fn(EXECUTE)

## `INTERPRET ( string:source -- )` interpret source code from string
def INTERPRET(vm):
    lexer.input(vm.pop().value)
    while True:
        if not WORD(vm): break
        if isinstance(vm.top(),Symbol):
            if FIND(vm): EXECUTE(vm)
F << Fn(INTERPRET)

## @}

# ################################# startup ##################################

while __name__ == '__main__':
    print F.dump(slots=None)
    F.push( String( raw_input('\ninfer> ') ) ) ; INTERPRET(F)

#}
