# https://ponyatov.quora.com/Homebrew-WebAssembly-compiler

# load LLVM binding library
import llvmlite.ir      as ir   # intermediate representation
import llvmlite.binding as llvm # LLVM interface

# import PLY (Python Lex-Yacc) library (c) David M. Beazley
import ply.lex  as lex
import ply.yacc as yacc

# LLVM must be initialized to required target architecture
# llvm.initialize()
llvm.initialize_native_target()
# llvm.initialize_native_asmprinter()

# compilation module
module = ir.Module(name='hello') ; print module
