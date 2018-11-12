
import ply.lex as lex

tokens = ['symbol']

t_ignore = ' \t\r\n'

def t_symbol(t):
    r'[a-zA-Z0-9_\?\.\:\;\+\-\*\/\^\@\!\<\>]+'
    return Symbol(t.value)

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()
