%{
#include "compiler.hpp"
%}

%option yylineno noyywrap

%%
#[^\n]*			{}						// line comments
[ \t\r\n]+		{}						// drop spaces

\.module		{return MODULE;}
\.target		{return TARGET;}
\.end			{return END;}

.				{yyerror("lexer");}		// any undetected char
