LLVM_VER	= 6.0.1
# 7.0.0 does not builds

LLVM		= llvm-$(LLVM_VER)
LLVM_GZ		= $(LLVM).src.tar.xz

PREFIX ?= /usr/local

CWD = $(CURDIR)
GZ	= $(CWD)/gz
SRC = $(CWD)/src
BLD = $(CWD)/build

WGET = wget -c -P $(GZ)

hello.log: hello.src ./compiler
	./compiler < $< > $@ && tail $(TAIL) $@ 

C = compiler.cpp compiler.yacc.cpp compiler.lex.cpp
H = compiler.hpp compiler.yacc.hpp
./compiler: $(C) $(H)
	$(CXX) $(CXXFLAGS) -o $@ $(C)
compiler.lex.cpp: compiler.lex
	flex -o $@ $<
compiler.yacc.cpp: compiler.yacc
	bison -o $@ $<

install: $(PREFIX)/bin/llc
#	$(MAKE) distclean
$(PREFIX)/bin/llc: $(BLD)/bin/llc
	cd $(BLD) ; sudo $(MAKE) install 

$(BLD)/bin/llc: $(BLD)/CMakeCache.txt
	cd $(BLD) ; $(MAKE) -j$(shell grep processor /proc/cpuinfo|wc -l )
$(BLD)/CMakeCache.txt: $(SRC)/$(LLVM).src/CMakeLists.txt
	rm -rf $(BLD) ; mkdir $(BLD) ; cd $(BLD) ;\
		cmake $(SRC)/$(LLVM).src \
			-DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$(PREFIX) \
			-DLLVM_TARGETS_TO_BUILD="X86"

src: $(SRC)/$(LLVM).src/CMakeLists.txt
$(SRC)/$(LLVM).src/CMakeLists.txt: $(GZ)/$(LLVM_GZ)
	mkdir -p $(SRC) ; cd $(SRC) ; xzcat $< | tar x && touch $@
$(GZ)/$(LLVM_GZ):
	mkdir -p $(GZ) ; $(WGET) -O $@ http://releases.llvm.org/$(LLVM_VER)/$(LLVM_GZ)

uninstall:
	rm -rf $(PREFIX)/bin/ll* $(PREFIX)/include/llvm* \
			$(PREFIX)/lib/*LLVM* $(PREFIX)/lib/libLTO* \
			$(PREFIX)/lib/BugpointPasses.so $(PREFIX)/lib/TestPlugin.so

distclean:
	rm -rf $(SRC) $(BLD)
