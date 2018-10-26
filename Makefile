all: doxy test.log

doxy:
	doxygen doxy.gen 1> /dev/null

test.log: kb.py test.src
	python $^ > $@ && tail $(TAIL) $@