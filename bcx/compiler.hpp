/// @file
/// @brief bytecode compiler headers

/// @defgroup bc bytecode compiler
/// @{

#ifndef _H_COMPILER
#define _H_COMPILER

#include <iostream>
#include <vector>
#include <map>

#include "bcx.h"

/// @defgroup parser lexer/parser interface
/// @{

										/// fetch next token from lexer
extern int yylex();
										/// current line in source file
extern int yylineno;
										/// last matched string in lexer
extern char *yytext;
										/// run parser
extern int yyparse();
										/// error callback
extern void yyerror(std::string msg);
#include "compiler.parser.hpp"

/// @}

/// @}

#endif // _H_COMPILER
