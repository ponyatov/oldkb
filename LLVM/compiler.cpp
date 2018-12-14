#include "compiler.hpp"

#define YYERR "\n\n"<< yylineno <<":"<< msg <<"["<< yytext <<"]\n\n"
void yyerror(std::string msg) {
	std::cout << YYERR; std::cerr << YYERR; exit(-1); }

llvm::LLVMContext llContext;
llvm::Module *llModule =NULL;
llvm::IRBuilder<> llBuilder(llContext);

std::map<std::string,std::string*> sym_strings;

int main() { return yyparse(); }
