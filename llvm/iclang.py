# LLVM-backed interpreter

# pip install --upgrade --user llvmlite

# https://ian-bertolacci.github.io/llvm/llvmlite/python/compilers/programming/2016/03/06/LLVMLite_fibonacci.html
from llvmlite import ir
from llvmlite import binding as llvm

llvm.initialize()
llvm.initialize_all_targets()
llvm.initialize_all_asmprinters()

target = llvm.Target.from_triple('wasm32') ; print 'target',target

module = ir.Module(name='fibonacci') ; print 'module',module

i32 = ir.IntType(32) ; print 'i32',i32
i64 = ir.IntType(64) ; print 'i64',i64

fn_int_to_int = ir.FunctionType(i32,[i32]) ; print 'fn_int_to_int',fn_int_to_int
