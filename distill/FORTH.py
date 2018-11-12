
###################################### classical stack banging ###############

################################### frame manipuations ########################

def ST(vm):
    obj = vm.pop() ; slot = vm.pop() ; vm.top()[slot.value] = obj
F << Fn(ST)
F['!'] = Fn(ST)

def LD(vm):
    slot = vm.pop()
    try: vm.push ( vm.top()[slot.value] )
    except KeyError: vm.push( slot )
F << Fn(LD)
F['@'] = Fn(LD)

def SUB(vm):
    obj = vm.pop() ; vm.top() << obj
F << Fn(SUB)
F['//'] = Fn(SUB)

def PUSH(vm):
    obj = vm.pop() ; vm.top().push(obj)
F << Fn(PUSH)
F['<<'] = Fn(PUSH)

def pDROP(vm):
    vm.top().drop()
F['.DROP'] = Fn(pDROP)

###################################### interpreter ############################

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

################################### system startup ############################

while __name__ == '__main__':
    print F.dump(slots=None)
    F.push( String( raw_input('\ninfer> ') ) ) ; INTERPRET(F)

## @}
