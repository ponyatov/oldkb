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

C = compiler.cpp parser.cpp lexer.cpp
H = compiler.hpp parser.hpp

CXXFLAGS	+= -I$(shell llvm-config --includedir )
L			+= $(shell llvm-config --libs core --system-libs )

./compiler: $(C) $(H) Makefile
	$(CXX) $(CXXFLAGS) -o $@ $(C) $(L) && ls -la $@
lexer.cpp: compiler.lex
	flex -o $@ $<
parser.cpp: compiler.yacc
	bison -o $@ $<

install: $(PREFIX)/bin/llc
#	$(MAKE) distclean

llvm: $(PREFIX)/bin/llvm-config
$(PREFIX)/bin/llvm-config: $(BLD)/bin/llvm-config
	cd $(BLD) ; sudo $(MAKE) install 
$(BLD)/bin/llvm-config: $(BLD)/CMakeCache.txt
	cd $(BLD) ; $(MAKE) -j$(shell grep processor /proc/cpuinfo|wc -l )
$(BLD)/CMakeCache.txt: $(SRC)/$(LLVM).src/CMakeLists.txt
	rm -rf $(BLD) ; mkdir $(BLD) ; cd $(BLD) ;\
		cmake $(SRC)/$(LLVM).src \
			-DCMAKE_BUILD_TYPE=MinSizeRel -DCMAKE_INSTALL_PREFIX=$(PREFIX) \
			-DLLVM_TARGETS_TO_BUILD="host"

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
	sudo rm -rf $(SRC) $(BLD)
