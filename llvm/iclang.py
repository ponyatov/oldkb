# LLVM-backed interpreter

# pip install --upgrade --user llvmlite

# https://ian-bertolacci.github.io/llvm/llvmlite/python/compilers/programming/2016/03/06/LLVMLite_fibonacci.html
from llvmlite import ir
from llvmlite import binding as llvm

llvm.initialize()
llvm.initialize_all_targets()
llvm.initialize_all_asmprinters()

# target = llvm.Target.from_triple('wasm32') ; print 'target',target
target = llvm.Target.from_triple('thumb') ; print 'target',target

module = ir.Module(name='fibonacci') ; print 'module',module

i32 = ir.IntType(32) ; print 'i32',i32
# i64 = ir.IntType(64) ; print 'i64',i64

fn_int_to_int = ir.FunctionType(i32,[i32]) ; print 'fn_int_to_int',fn_int_to_int

import ply.lex  as lex
import ply.yacc as yacc

tokens = ['PRINT','NUM','ADD','SUB','MUL','DIV']

t_ignore = ' \t\r\n'

t_PRINT = 'print'
t_NUM = '[0-9]+'
t_ADD = '\+'
t_MUL = '\*'

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()

lexer.input('''

print 1+2*3

''')
while True:
    token = lexer.token()
    if not token: break
    print token
