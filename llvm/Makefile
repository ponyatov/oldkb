
LITE_VER = v0.26.0dev0

CWD = $(CURDIR)

.PHONY: all build lite clean distclean

all: build lite

clean:
	rm -rf build
	
distclean: clean
	rm -rf llvm

build: /usr/local/bin/llc
/usr/local/bin/llc: llvm/README.txt
	cd $@ ; cmake -G "Unix Makefiles" \
		-DCMAKE_INSTALL_PREFIX=/usr/local \
		-DCMAKE_BUILD_TYPE=Release \
		-DLLVM_TARGETS_TO_BUILD="ARM;Mips;WebAssembly;X86" \
	../llvm && $(MAKE) && sudo $(MAKE) install

llvm/README.txt:
	git clone --depth=1 https://git.llvm.org/git/llvm.git/
	cd llvm ; git config branch.master.rebase true

lite: llvmlite/README.rst
llvmlite/README.rst:
	git clone -b $(LITE_VER) --depth=1 https://github.com/numba/llvmlite.git
