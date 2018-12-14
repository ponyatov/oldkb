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

[a-zA-Z0-9_]+	{yylval.s = yytext; return SYM;}

.				{yyerror("lexer");}		// any undetected char
