# https://www.youtube.com/playlist?list=PLddc343N7YqgYvD0Kfc91QUcssH_5_sn8

# unit calculator

# lexer

import ply.lex  as lex
import cmd

tokens = ['sym','int','num','unit','add','sub','mul','div','pow','eq']

t_ignore = ' \t\r\n'

# operators
def t_add(t):
    r'\+'
    return t
def t_sub(t):
    r'\-'
    return t
def t_mul(t):
    r'\*'
    return t
def t_div(t):
    r'\/'
    return t
def t_pow(t):
    r'\^'
    return t

def t_eq(t):
    r'\='
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

precedence = (
    ('left','add','sub'),
    ('left','mul','div'),
    ('right','pow'),
    )

def p_none(p):
    ' REPL :'
def p_recur(p):
    ' REPL : REPL ex '
    print '      e',p[2]
    print 'eval(e)',evalAST(p[2])
    
# variable memory
M = {}

def p_ex_sym(p):
    ' ex : sym '
    try:
        p[0] = M[p[1]]
    except KeyError:
        p[0] = None
        
def p_ex_set(p):
    ' ex : sym eq ex '
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
    ' un : un pow int'
    p[0] = {p[1]:p[3]}

def p_error(p): raise SyntaxError(p) 

parser = yacc.yacc(debug=False,write_tables=False)

# evaluator

def evalAST(e):
    if isinstance(e,(int,float)): return (e,{})
    return e

while True:
    parser.parse(raw_input('\nbodik> '))
