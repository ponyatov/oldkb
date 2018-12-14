#ifndef _COMPILER_H
#define _COMPILER_H

#include <iostream>

extern int yylex();						// lexer/parser interface
extern int yylineno;
extern char* yytext;
extern int yyparse();
extern void yyerror(std::string);
#include "parser.hpp"

#endif // _COMPILER_H
