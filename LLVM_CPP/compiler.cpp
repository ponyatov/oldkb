#include "compiler.hpp"

#define YYERR "\n\n"<< yylineno <<":"<< msg <<"["<< yytext <<"]\n\n"
void yyerror(std::string msg) {
	std::cout << YYERR; std::cerr << YYERR; exit(-1); }

int main() {
	while (yylex()) { std::cout << yytext << std::endl; }
}
