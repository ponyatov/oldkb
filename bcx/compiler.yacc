%{
#include "compiler.hpp"
%}

%defines %union { uint8_t op; }

%token pEND pVM
%token <op> CMD0

%%
REPL :
REPL : REPL pVM		{ VM(); }
REPL : REPL pEND	{ DUMP(); BYE(); }
REPL : REPL CMD0	{ M[Cp++] = $2; }
