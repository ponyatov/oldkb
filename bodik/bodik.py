# https://www.youtube.com/playlist?list=PLddc343N7YqgYvD0Kfc91QUcssH_5_sn8

# lexer

import ply.lex  as lex

tokens = ['sym','num','op','unit']

t_ignore = ' \t\r\n'

def t_op(t):
    r'[\+\-\*\/\^\=]'
    return t

def t_num(t):
    r'[0-9]+(\.[0-9]+)?'
    t.value = float(t.value) ; return t

def t_unit(t):
    r'kg|m|s'
    return t

def t_sym(t):
    r'[a-zA-Z0-9_]+'
    return t

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()

# parser

import ply.yacc as yacc

def p_none(p):
    ' REPL :'
def p_recur(p):
    ' REPL : REPL ex '
    print p[2]
    
def p_ex_num(p):
    ' ex : num'
    p[0] = p[1]

def p_error(p): raise SyntaxError(p) 

parser = yacc.yacc(debug=False,write_tables=False)

while True:
    parser.parse(raw_input('\nbodik> '))
