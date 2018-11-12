hello: hello.wasm

%.wasm: %.wat Makefile
	wabt/wat2wasm -o $@ $< && wabt/wasm-objdump -x -h -d -s $@ > $@.dump

