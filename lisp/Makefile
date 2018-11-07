lisp.log: ./lisp lisp.test Makefile
	./lisp > $@ & tail $(TAIL) $@
	
C = lisp.c lisp.parser.c lisp.lexer.c
H = lisp.h lisp.parser.h

CFLAGS += -std=c89 -pedantic

./lisp: $(C) $(H) Makefile 
	$(CC) $(CFLAGS) -o $@ $(C)
lisp.lexer.c: lisp.l
	flex -o $@ $<
lisp.parser.c: lisp.y
	bison -o $@ $<
