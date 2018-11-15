all: doxy static/D3.js

doxy:
	rm docs/* ; doxygen doxy.gen 1>/dev/null

static/D3.js:
	wget -c -O $@ http://d3js.org/d3.v3.min.js

merge:
	git checkout dev doxy.gen sym.py forth.py parser.py web.py gui.py \
						doxy.gen doc db static templates
	$(MAKE) doxy
