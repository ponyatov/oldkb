all: doxy test.log

doxy:
	doxygen doxy.gen 1> /dev/null

test.log: pp.py test.src
	python $^ > $@.log && tail $(TAIL) $@