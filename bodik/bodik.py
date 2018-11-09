# https://www.youtube.com/playlist?list=PLddc343N7YqgYvD0Kfc91QUcssH_5_sn8

import ply.lex  as lex

tokens = ['sym','num','op']

t_ignore = ' \t\r\n'

def t_op(t):
    r'[\+\-\*\/\^\=]'
    return t

def t_num(t):
    r'[0-9]+'
    return t

def t_sym(t):
    r'[a-zA-Z0-9_]+'
    return t

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()

while True:
    lexer.input(raw_input('\nbodik> '))
    while True:
        token = lexer.token()
        if not token: break
        print token
