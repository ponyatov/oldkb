#ifndef _COMPILER_H
#define _COMPILER_H

#include <iostream>
										// LLVM structures
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Support/raw_ostream.h"

extern llvm::LLVMContext llContext;
extern llvm::Module *llModule;
extern llvm::IRBuilder<> llBuilder;

extern std::map<std::string,std::string*> sym_strings;

extern int yylex();						// lexer/parser interface
extern int yylineno;
extern char* yytext;
extern int yyparse();
extern void yyerror(std::string);
#include "parser.hpp"

#endif // _COMPILER_H
