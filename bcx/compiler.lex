%{
#include "compiler.hpp"
%}

%option noyywrap yylineno

%%
[\#\\][^\n]*		{ }						// line comment

nop					{ yylval.op = op_NOP; return CMD0; }
bye					{ yylval.op = op_BYE; return CMD0; }

.vm					{ return pVM; }
.end				{ return pEND; }

[ \t\r\n]+			{}						// drop spaces
.					{ yyerror("lexer");	}	// undetected char
