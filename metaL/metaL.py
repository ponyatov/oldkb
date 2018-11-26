# metaLanguage engine: FORTH in Python -> ANSI'C

import os,sys,dill,gzip

class Obj:
    # construct with name
    def __init__(self,V):
        self.type = self.__class__.__name__.lower() ; self.value = V
        self.attr = {} ; self.nest = []
        
    # print object
    def __repr__(self):
        return self.dump()
    def dump(self,depth=0,prefix=''):
        S = self.pad(depth) + self.head(prefix)
        for i in self.attr: S += self.attr[i].dump(depth+1,prefix='%s = '%i)
        for j in self.nest: S += j.dump(depth+1)
        return S
    def head(self,prefix=''):
        return '%s<%s:%s>' % (prefix, self.type, self.value)
    def pad(self,N):
        return '\n' + '\t'*N

    # attr{}    
    def __setitem__(self,key,obj): self.attr[key] = obj ; return self
    def __getitem__(self,key): return self.attr[key]
    def __lshift__(self,obj):
        if isinstance(obj,Obj): self[obj.value] = obj ; return self
        if callable(obj): return self << Fn(obj)
        raise TypeError(obj)
    # nest[] as stack
    def dropall(self): self.nest = []
    def push(self,obj): self.nest.append(obj) ; return self
    def pop(self): return self.nest.pop()
    def top(self): return self.nest[-1]
    def dup(self): self.push(self.top())
    def drop(self): self.pop()
    def swap(self): B = self.pop() ; A = self.pop() ; self.push(B) ; self.push(A)
    def over(self): self.push(self.nest[-2])
    def press(self): del self.nest[-2]

    
class Sym(Obj): pass
class Str(Obj): pass
class Num(Obj): pass
class Int(Num): pass

class StacK(Obj): pass
class Map(Obj): pass

class Fn(Obj):
    def __init__(self,F): Obj.__init__(self, F.__name__) ; self.fn = F
    def __call__(self): self.fn()

# stack
S = StacK('data')

# vocabulary
W = Map('FORTH')

W['?'] = W['WORDS'] = Fn(W.dump)

W['.'] = W['DROPALL'] = Fn(S.dropall)
W['DUP']   = Fn(S.dup)
W['DROP']  = Fn(S.drop)
W['SWAP']  = Fn(S.swap)
W['OVER']  = Fn(S.over)
W['PRESS'] = Fn(S.press)

def SAVE():
    with gzip.GzipFile(sys.argv[0]+'.db','wb',9) as db: dill.dump(W,db)
W << SAVE

def LOAD():
    with gzip.open(sys.argv[0]+'.db','rb',9) as db: W = dill.load(db)

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
W << WORD
    
def FIND():
    token = S.pop()
    try:
        S.push(W[token.value]) ; return True
    except KeyError:
        try: S.push(W[token.value.upper()]) ; return True
        except KeyError: S.push(token) ; return False
W << FIND
    
def EXECUTE():
    S.pop() ()
W << EXECUTE
    
def INTERPRET(SRC):
    lexer.input(SRC)
    while True:
        if not WORD(): break
        if FIND(): EXECUTE()

# REPL
while True: print S ; INTERPRET(raw_input('\nok> '))
