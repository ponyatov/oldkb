
from sym import *

############################# FORTH Virtual Machine ###########################

class FORTH(VM):
    def add(self): B = self.pop() ; A = self.pop() ; self.push(A.add(B))
    def sub(self): B = self.pop() ; A = self.pop() ; self.push(A.sub(B))
    def mul(self): B = self.pop() ; A = self.pop() ; self.push(A.mul(B))
    def div(self): B = self.pop() ; A = self.pop() ; self.push(A.div(B))
    def pow(self): B = self.pop() ; A = self.pop() ; self.push(A.pow(B))
    def int(self): self.push(self.pop().int())
    def num(self): self.push(self.pop().num())

F = FORTH('vm')

F['vm'] = F

##################################### debug ###################################

def BYE(vm): sys.exit(0)
F << Fn(BYE)

def q(vm): print vm.pop()
F['?'] = Fn(q)

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

def ADD(vm): vm.add()
F << Fn(ADD)
F['+'] = Fn(ADD)

def SUB(vm): vm.sub()
F << Fn(SUB)
F['-'] = Fn(SUB)

def MUL(vm): vm.mul()
F << Fn(MUL)
F['*'] = Fn(MUL)

def DIV(vm): vm.div()
F << Fn(DIV)
F['/'] = Fn(DIV)

def POW(vm): vm.pow()
F << Fn(POW)
F['^'] = Fn(POW)

def INT(vm): vm.int()
F << Fn(INT)

def NUM(vm): vm.num()
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
