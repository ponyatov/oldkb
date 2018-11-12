/* minimal Lisp in ANSI C                   */
/* http://www.buildyourownlisp.com/contents */

#ifndef _H_LISP
#define _H_LISP

#define URL "https://github.com/ponyatov/kb/tree/dev/lisp"

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include <readline/readline.h>
#include <readline/history.h>

extern int yylex();
extern int yylineno;
extern char *yytext;
extern FILE *yyin;
extern int yyparse();
extern void yyerror(char*);
#include "lisp.parser.h"

#endif /* _H_LISP */
