#ifndef _COMPILER_H
#define _COMPILER_H

#include <iostream>

extern int yylex();
extern int yylineno;
extern char* yytext;
extern void yyparse();
extern void yyerror(std::string);

#endif // _COMPILER_H
