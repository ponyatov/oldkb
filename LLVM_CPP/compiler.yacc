%{
#include "compiler.hpp"
%}

%defines %union { char *a; std::string *s; }

%token MODULE TARGET END
%token <a> SYM 
%token <s> STR
%token EQ

%%
REPL :
REPL : REPL MODULE SYM	{ std::cout << "module:" << $3 << std::endl;
							llModule = new llvm::Module($3, llContext); }
REPL : REPL TARGET SYM	{ std::cout << "target:" << $3 << std::endl; }
REPL : REPL END			{ 

  llvm::FunctionType *funcType = 
      llvm::FunctionType::get(llBuilder.getVoidTy(),false);//Int64Ty(), false);
  llvm::Function *mainFunc = 
      llvm::Function::Create(funcType, llvm::Function::ExternalLinkage, "main", llModule);
      
  llvm::BasicBlock *entry = llvm::BasicBlock::Create(llContext, "entry", mainFunc);
  llBuilder.SetInsertPoint(entry);      
  
  for(auto it=sym_strings.begin(),e=sym_strings.end();it!=e;it++) {
  	llBuilder.CreateGlobalStringPtr(*(it->second));
  }
  //llvm::Value *helloWorld = llBuilder.CreateGlobalStringPtr("hello world!\n");
  
  llBuilder.CreateRetVoid();
      
      std::string Str; llvm::raw_string_ostream OS(Str);
							OS << *llModule; OS.flush();
							std::cout << Str; exit(0); }

REPL : REPL SYM EQ STR	{ sym_strings[$2] = $4; }
