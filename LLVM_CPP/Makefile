LLVM_VER	= 7.0.0
LLVM		= llvm-$(LLVM_VER)
LLVM_GZ		= $(LLVM).src.tar.xz

PREFIX ?= /usr/local

CWD = $(CURDIR)
GZ	= $(CWD)/gz
SRC = $(CWD)/src

WGET = wget -c -P $(GZ)

uninstall:
	rm -rf $(PREFIX)/bin/ll* $(PREFIX)/include/llvm* \
			$(PREFIX)/lib/*LLVM* $(PREFIX)/lib/libLTO* \
			$(PREFIX)/lib/BugpointPasses.so $(PREFIX)/lib/TestPlugin.so

src: $(SRC)/$(LLVM).src/README.txt
$(SRC)/$(LLVM).src/README.txt: $(GZ)/$(LLVM_GZ)
	mkdir -p $(SRC) ; cd $(SRC) ; xzcat $< | tar x && touch $@
$(GZ)/$(LLVM_GZ):
	mkdir -p $(GZ) ; $(WGET) -O $@ http://releases.llvm.org/$(LLVM_VER)/$(LLVM_GZ)
