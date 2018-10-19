hello: hello.wasm

%.wasm: %.wat
	wabt/wat2wasm -o $@ $^
