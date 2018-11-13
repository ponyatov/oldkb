
CWD = $(CURDIR)

.PHONY: build

build: llvm/README.txt
	rm -rf $@ ; mkdir $@ ; cd $@ ; cmake -G "Unix Makefiles" \
		-DCMAKE_INSTALL_PREFIX=$(CWD)/install \
		-DCMAKE_BUILD_TYPE=Release \
		-DLLVM_TARGETS_TO_BUILD="ARM;Mips;WebAssembly;X86" \
	../llvm && $(MAKE) && $(MAKE) install

llvm/README.txt:
	git clone --depth=1 https://git.llvm.org/git/llvm.git/
	cd llvm ; git config branch.master.rebase true
