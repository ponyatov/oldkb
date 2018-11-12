all: doxy static/D3.js

doxy:
	doxygen doxy.gen 1>/dev/null

static/D3.js:
	wget -c -O $@ http://d3js.org/d3.v3.min.js
