%{
#include "lisp.h"
%}

%defines %union { char* atom; }

%token <atom> ATOM

%%
REPL : | REPL ATOM	{ printf("\n<%s>\n",$2); }
