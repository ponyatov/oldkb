/// @file
/// @brief bytecode compiler C++ code

#include "compiler.hpp"

#define YYERR "\n\n" << yylineno << ":" << msg << "[" << yytext << "]\t\n"

void yyerror(std::string msg) { std::cout << YYERR; std::cerr << YYERR ; exit(-1); }

int main() { return yyparse(); }
