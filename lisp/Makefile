./lisp: lisp.c lisp.lexer.c lisp.parser.c 
	$(CC) -o $@ $^
lisp.lexer.c: lisp.l
	flex -o $@ $<
lisp.parser.c: lisp.y
	bison -o $@ $<
	