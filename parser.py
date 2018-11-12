## @file
## @brief Syntax parser (primitive lexer-only) /@ref ply/

## @defgroup parser Syntax parser
## @brief primitive lexer-only parser using @ref ply
## @{ 

from sym import *

import ply.lex as lex

tokens = ['symbol','number','integer','hex','bin']

t_ignore = ' \t\r\n'

def t_number(t):
    r'[\+\-]?[0-9]*\.[0-9]+([eE][\+\-]?[0-9]+)?'
    return Number(t.value)

def t_expint(t):
    r'[\+\-]?[0-9]+[eE][\+\-]?[0-9]+?'
    return Number(t.value)

def t_hex(t):
    r'0x[0-9a-fA-F]+'
    return Hex(t.value)

def t_bin(t):
    r'0b[01]+'
    return Bin(t.value)
    
def t_integer(t):
    r'[\+\-]?[0-9]+'
    return Integer(t.value)

def t_symbol(t):
    r'[a-zA-Z0-9_\?\.\:\;\+\-\*\/\%\^\@\!\<\>]+'
    return Symbol(t.value)

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()

## @}
