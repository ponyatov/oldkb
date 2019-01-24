ifeq ($(OS),Windows_NT)
	EXE = .exe
else
	EXE =
endif

FORTH.log: FORTH.src ./compiler$(EXE)
	./compiler$(EXE) < $< > $@ && tail $(TAIL) $@

C = bcx.c compiler.cpp compiler.parser.cpp compiler.lexer.cpp 
H = bcx.h compiler.hpp compiler.parser.hpp

./compiler$(EXE): $(C) $(H)
	$(CXX) $(CXXFLAGS) -o $@ $(C)
	
compiler.lexer.cpp: compiler.lex
	flex -o $@ $<
	
compiler.parser.cpp: compiler.yacc
	bison -o $@ $<

doxy:
	rm -rf docs ; doxygen doxy.gen 1> /dev/null

clean:
	rm -rf compiler.yacc.?pp compiler.lexer.cpp