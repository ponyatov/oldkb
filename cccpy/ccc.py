# metaprogramming engine: FORTH in Python -> ANSI'C

# stack
S = []

# vocabulary
W = {}

# print stack
def q(): print S
W['?'] = q

def INTERPRET(SRC):
    lexer.input(SRC)
    while True:
        if not WORD(): break
        print S

# REPL
while True: q() ; INTERPRET(raw_input('ok> '))
                            