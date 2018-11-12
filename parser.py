
from sym import *

import ply.lex as lex

tokens = ['symbol','number','integer']

t_ignore = ' \t\r\n'

def t_integer(t):
    r'[\+\-]?[0-9]+'
    return Integer(t.value)

def t_symbol(t):
    r'[a-zA-Z0-9_\?\.\:\;\+\-\*\/\^\@\!\<\>]+'
    return Symbol(t.value)

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()
