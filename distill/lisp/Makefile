lisp.log: ./lisp lisp.test Makefile
	./lisp > $@ & tail $(TAIL) $@
	
cli: ./lisp
	./lisp
	
C  = lisp.c lisp.parser.c lisp.lexer.c
H  = lisp.h lisp.parser.h

L += -lreadline

CFLAGS += -std=c89 -pedantic

./lisp: $(C) $(H) Makefile 
	$(CC) $(CFLAGS) -o $@ $(C) $(L)
lisp.lexer.c: lisp.l
	flex -o $@ $<
lisp.parser.c: lisp.y
	bison -o $@ $<
