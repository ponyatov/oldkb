# LLVM-backed interpreter

# pip install --upgrade --user llvmlite

# https://ian-bertolacci.github.io/llvm/llvmlite/python/compilers/programming/2016/03/06/LLVMLite_fibonacci.html
from llvmlite import ir
from llvmlite import binding as llvm

# ################################# module ####################################

llvm.initialize()
# llvm.initialize_all_targets()
# llvm.initialize_all_asmprinters()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

# target = llvm.Target.from_triple('wasm32') ; print 'target',target
# target  = llvm.Target.from_triple('thumb-none-eabi') ; print 'target',target,target.triple
target  = llvm.Target.from_default_triple() ; print 'target',target
machine = target.create_target_machine() ; print 'machine',machine

# JIT engine
jit = llvm.create_mcjit_compiler(llvm.parse_assembly(''),machine) ; print 'jit',jit

module = ir.Module(name='fibonacci')

# ################################# types #####################################
void = ir.VoidType()
float = ir.FloatType()
i8,i16,i32,i64 = map(ir.IntType,[8,16,32,64])

fn_int_to_int = ir.FunctionType(i32,[i32]) ; print 'fn_int_to_int',fn_int_to_int

# ################################# parser ####################################

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

# #############################################################################

lexer.input('''

print 1+2*3

''')
while True:
    token = lexer.token()
    if not token: break
    print token

# #############################################################################

print '-'*77
print module
print llvm.parse_assembly(str(module))

