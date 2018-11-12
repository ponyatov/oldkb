%{
#include "lisp.h"
%}

%option noyywrap yylineno

%%

^#!.*\n		{}		/* drop script heading */
