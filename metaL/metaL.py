# metaLanguage engine: FORTH in Python -> ANSI'C

class Obj:
    # construct with name
    def __init__(self,V):
        self.type  = self.__class__.__name__.lower()
        self.value = V
        self.attr  = {}
        self.nest  = []
        
    # print object
    def __repr__(self):
        return self.dump()
    def dump(self,depth=0):
        S = self.pad(depth) + self.head()
        return S
    def head(self,prefix=''):
        return '%s<%s:%s>' % (prefix, self.type, self.value)
    def pad(self,N):
        return '\n' + '\t'*N

    # attr{}    
    def __setitem__(self,key,obj): self.attr[key] = obj ; return self
    def __getitem__(self,key): return self.attr[key]
        
    # nest[] as stack
    def dropall(self): self.nest = []
    def push(self,obj): self.nest.append(obj) ; return self
    def pop(self): return self.nest.pop()
    def top(self): return self.nest[-1]
    
class Sym(Obj): pass
class Str(Obj): pass
class Num(Obj): pass
class Int(Num): pass

class StacK(Obj): pass
class Map(Obj): pass

# stack
S = StacK('data')

# vocabulary
W = Map('FORTH')

W['?'] = W['WORDS'] = W.dump

W['.'] = W['DROPALL'] = S.dropall 

import ply.lex as lex

tokens = ['sym','num','str']

t_ignore = ' \t\r\n'

def t_num(t):
    r'[0-9]+'
    return Num(t.value)
def t_sym(t):
    r'[^ \t\r\n]+'
    return Sym(t.value)

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()

def WORD():
    token = lexer.token()
    if not token: return False
    S.push(token) ; return True
    
def FIND():
    token = S.pop()
    try: S.push(W[token.value]) ; return True
    except KeyError: S.push(token) ; return False
    
def EXECUTE():
    S.pop() ()
    
def INTERPRET(SRC):
    lexer.input(SRC)
    while True:
        if not WORD(): break
        if FIND(): EXECUTE()

# REPL
while True: print S ; INTERPRET(raw_input('\nok> '))
                            