class Term:
    def __init__(self,V):
        self.value = V
        self.nest = []
        self.attr ={}
        
    ## iterator
    def __iter__(self): return self.iter
    def iter(self):
        for j in self.nest: yield j

    def __repr__(self): return self.dump()
    def dump(self): return '%s : %s'% (self.value , self.nest)
        
print Term('x')

def Pers(name):
    yield 'A'
    yield 'B'
    yield 'C'
    
class oPers(Term):
    def __init__(self,V):
        Term.__init__(self, V)
        self.nest = ['A','B','C']

for p in oPers('pers'):
    print p