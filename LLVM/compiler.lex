%{
#include "compiler.hpp"

std::string* LexString;

%}

%option yylineno noyywrap

%s str

%%
#[^\n]*			{}						// line comments
[ \t\r\n]+		{}						// drop spaces

\.module		{return MODULE;}
\.target		{return TARGET;}
\.end			{return END;}

<INITIAL>\"		{BEGIN(str); LexString = new std::string(""); }
<str>\"			{BEGIN(INITIAL); yylval.s = LexString; return STR;}
<str>.			{*LexString += yytext;}

\=				{return EQ;}

[a-zA-Z0-9_]+	{yylval.a = yytext; return SYM;}

.				{yyerror("lexer");}		// any undetected char
