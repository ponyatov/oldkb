%{
#include "compiler.hpp"
%}

%defines %union { char *s; }

%token MODULE TARGET END
%token <s> SYM

%%
REPL : MODULE SYM		{ std::cout << "module:" << $2 << std.endl; }
