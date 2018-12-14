%{
#include "compiler.hpp"
%}

%defines %union { char *s; }

%token MODULE TARGET END
%token <s> SYM

%%
REPL :
REPL : REPL MODULE SYM	{ std::cout << "module:" << $3 << std::endl; }
REPL : REPL TARGET SYM	{ std::cout << "target:" << $3 << std::endl; }
REPL : REPL END			{ exit(0); }
