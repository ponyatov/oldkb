
LLVM_VER = 6.0.1
# 6.0.x required for llvmlite
LITE_VER = v0.26.0dev0

PREFIX ?= /usr/local

LLCONFIG = $(PREFIX)/bin/llvm-config

CWD = $(CURDIR)

GZ	?= $(HOME)/gz

.PHONY: all build lite clean distclean uninstall uninstall-llvm uninstall-lite

all: build lite

clean:
	rm -rf build
	
distclean: clean
	rm -rf llvm llvmlite
	
uninstall: uninstall-llvm
uninstall-llvm:
	rm -rf \
		$(PREFIX)/bin/llvm* $(PREFIX)/bin/ll? \
		$(PREFIX)/include/llvm* $(PREFIX)/lib/cmake/llvm

build: $(LLCONFIG)
$(LLCONFIG): llvm/README.txt
	rm -rf build ; mkdir build ; cd build ; cmake -G "Unix Makefiles" \
		-DCMAKE_INSTALL_PREFIX=$(PREFIX) \
		-DCMAKE_BUILD_TYPE=RelWithDebInfo \
		-DLLVM_TARGETS_TO_BUILD="" \
		-DLLVM_EXPERIMENTAL_TARGETS_TO_BUILD="WebAssembly" \
		-DLLVM_OPTIMIZED_TABLEGEN=Y \
	../llvm && $(MAKE) && sudo $(MAKE) install
#		-DLLVM_TARGETS_TO_BUILD="ARM;Mips;X86" \

LLVM	= llvm-$(LLVM_VER)
LLVM_GZ = $(LLVM).src.tar.xz
llvm/README.txt: $(GZ)/$(LLVM_GZ)
	xzcat $< | tar x && rm -rf llvm && mv $(LLVM).src llvm && touch $@
$(GZ)/$(LLVM_GZ):
	mkdir -p $(GZ) ; wget -c -O $@ http://releases.llvm.org/$(LLVM_VER)/$(LLVM_GZ)
#	git clone -b $(LLVM_VER) --depth=1 https://git.llvm.org/git/llvm.git/
#	cd llvm ; git config branch.master.rebase true

lite: llvmlite/README.rst
	cd llvmlite ; echo LLVM_CONFIG=$(LLCONFIG) python setup.py build
llvmlite/README.rst:
	git clone -b $(LITE_VER) --depth=1 https://github.com/numba/llvmlite.git
