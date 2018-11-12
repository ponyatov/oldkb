
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

## @}
