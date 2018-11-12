
from sym import *

############################# FORTH Virtual Machine ###########################

class FORTH(VM): pass

F = FORTH('vm')

F['vm'] = F

##################################### debug ###################################

def BYE(vm): sys.exit(0)
F << Fn(BYE)

def q(vm): print vm.pop()
F['?'] = Fn(q)

def WORDS(vm): vm.push(vm.slots())
F << Fn(WORDS)

##################################### stack ###################################

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

#################################### math #####################################

def ADD(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.add(B))
F << Fn(ADD)
F['+'] = Fn(ADD)

def SUB(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.sub(B))
F << Fn(SUB)
F['-'] = Fn(SUB)

def MUL(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.mul(B))
F << Fn(MUL)
F['*'] = Fn(MUL)

def DIV(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.div(B))
F << Fn(DIV)
F['/'] = Fn(DIV)

def MOD(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.mod(B))
F << Fn(MOD)
F['%'] = Fn(MOD)

def POW(vm): B = vm.pop() ; A = vm.pop() ; vm.push(A.pow(B))
F << Fn(POW)
F['^'] = Fn(POW)

def INT(vm): vm.push(vm.pop().int())
F << Fn(INT)

def NUM(vm): vm.push(vm.pop().num())
F << Fn(NUM)

################################## interpreter ################################

from parser import *

def WORD(vm):
    token = lexer.token()
    if not token: return False
    vm.push( token ) ; return True
F << Fn(WORD)
    
def FIND(vm):
    token = vm.pop()
    try: vm.push( vm[token.value] ) ; return True
    except KeyError:
        try: vm.push( vm[token.value.upper()] ) ; return True
        except KeyError:       vm.push( token ) ; return False
F << Fn(FIND)
    
def EXECUTE(vm):
    if callable(vm.top()): vm.pop() (vm)
F << Fn(EXECUTE)

def INTERPRET(vm):
    lexer.input(vm.pop().value)
    while True:
        if not WORD(vm): break
        if isinstance(vm.top(),Symbol):
            if FIND(vm): EXECUTE(vm)
F << Fn(INTERPRET)

#################################### startup ##################################

while __name__ == '__main__':
    print F.dump(slots=None)
    F.push( String( raw_input('\ninfer> ') ) ) ; INTERPRET(F)
