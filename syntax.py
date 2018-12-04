## @file
## @brief Syntax parser (primitive lexer-only) /@ref ply/

## @defgroup parser Syntax parser
## @ingroup interpret
## @brief primitive lexer-only parser using @ref ply
## @{ 

from sym import *

import ply.lex as lex

## parse directly into primitive @ref sym objects
tokens = ['symbol','string','number','integer','hex','bin','url']

## @name string
## @{

## laxer states (for string parsing)
states = (('str','exclusive'),)

t_str_ignore = ''

def t_string(t):
    r'\''
    t.lexer.string = ''
    t.lexer.push_state('str')
def t_str_string(t):
    r'\''
    t.lexer.pop_state()
    return String(t.lexer.string)
def t_str_tab(t):
    r'\\t'
    t.lexer.string += '\t'
def t_str_lf(t):
    r'\\n'
    t.lexer.string += '\n'
def t_str_char(t):
    r'.'
    t.lexer.string += t.value

## @}

## drop spaces
t_ignore = ' \t\r\n'

## @name numbers
## @{

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

## @}

def t_url(t):
	r'https?://[a-zA-Z0-9_\.\/\?\=]+'
	return Url(t.value)

def t_symbol(t):
    r'[a-zA-Z0-9_\?\.\:\;\+\-\*\/\%\^\@\!\$\<\>]+'
    return Symbol(t.value)

## lexer error callback
def t_ANY_error(t): raise SyntaxError(t)

lexer = lex.lex()

## @}
