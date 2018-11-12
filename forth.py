
from sym import *

############################# FORTH Virtual Machine ###########################

F = VM('FORTH')

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

#################################### startup ##################################

if __name__ == '__main__':
    print F
