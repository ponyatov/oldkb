# https://www.youtube.com/playlist?list=PLddc343N7YqgYvD0Kfc91QUcssH_5_sn8

# lexer

import ply.lex  as lex

tokens = ['sym','int','num','op','unit']

t_ignore = ' \t\r\n'

# operator
def t_op(t):
    r'[\+\-\*\/\^\=]'
    return t

# number
def t_num(t):
    r'[0-9]*\.[0-9]+'
    t.value = float(t.value) ; return t
    
# integer
def t_int(t):
    r'[0-9]+'
    t.value = int(t.value) ; return t

# symbol (variable name)
def t_sym(t):
    r'[a-zA-Z0-9_]+'
    # is measurement unit ?
    if t.value in ['kg','m','s']:
        t.type = 'unit'
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
    
# variable memory
M = {}

def p_ex_sym(p):
    ' ex : sym '
    try:
        p[0] = M[p[1]]
    except KeyError:
        p[0] = None
        
def p_ex_set(p):
    ' ex : sym op ex '
    if p[2] != '=': raise SyntaxError(p[2])
    p[0] = M[p[1]] = p[3] ; print M
        
# numeric value
def p_ex_val(p):
    ' ex : val'
    p[0] = p[1]
    
def p_ex_int(p):
    ' val : int'
    p[0] = p[1]
def p_ex_num(p):
    ' val : num'
    p[0] = p[1]
    
# value with units
def p_ex_epsilon(p):
    ' ex : ex un '
    p[0] = (p[1],p[2])
    
def p_un(p):
    ' un : unit '
    p[0] = p[1]
def p_un_pow(p):
    ' un : un op int'
    if p[2] == '^':
        p[0] = {p[1]:p[3]}
    else:    
        p[0] = (p[2],p[1],p[3])

def p_error(p): raise SyntaxError(p) 

parser = yacc.yacc(debug=False,write_tables=False)

while True:
    parser.parse(raw_input('\nbodik> '))
