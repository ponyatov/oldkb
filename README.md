# 
# object/graph/knowledge database

* @ref kb based on Marvin Minsky's
[Frame Model](https://en.wikipedia.org/wiki/Frame_(artificial_intelligence)
<br>with some adaptation for modern computing and programming languages
* [Logical programming](@ref logic) subsystem for generic AI applications
* powered by [symbolic system](@ref sym) object engine written in Python
* [kb/FORTH](@ref kbf) language used as easy to write command shell with
* [Tree script](@ref ts) extension for infix syntax & tree-based homoiconicity
* [Python persistence](@ref pp) used for knowledge database storage 

(c) Dmitry Ponyatov <<dponyatov@gmail.com>> , All rights reserved

github: https://github.com/ponyatov/kb

manual: https://ponyatov.github.io/kb

# FORTHodoxal [meta]programming system

What we want to have is some interactive system able to let us
construct software in high-level terms like data flows, deploy schemas, 
generic objects like queues, stacks, objects, databases, use cases and so on.
And there is one thing was not understood by many many experimental and 
orthodoxal programming language designers: _language manual must be 
**implementation manual** guides the user toward his own fork of 
the same language_. The key is no one experimental language can't contend 
with mainstream leaders like C++, Java, Python and HTML/JS Web domain. 
And it is not required: **new language must complement them in symbiosis**:
any programmer must be able to integrate *multiparadigm control & programming
language* into an arbitrary program or software system.

This project is about implementing tiny @ref kbf -inspired script language 
system for @ref meta.

The idea is about making some ultra high-level system lets 
* describe templates of software design in generic terms, objects, 
algorithm specifications, *code snippets*, and *generic programming* models
* generate source code for a wide range of target mainstream languages 
and runtime environments (OSes, frameworks, platforms,..)
* finally, the proof of concept is a _metacircular description of metasystem_ 
itself allows to bootstrap it in portable and transparent way

The base for the bootstrap process is tiny virtual machine written in Python. 
It is minimalistic for porting simplicity, and this manual describes 
most parts of it to let you reimplement it yourself in a way *you* want.
I purposely removed most of the complicated things described in the 
[metacircular knowledge base](@ref metakb) to highlight a few key elements, 
and do not overload the intro manual with details.

## web interface

* run `web.py` uses Flask framework
* @ref kiosk

## wxWidgets
### native client GUI

`gui.py` implements native client GUI to run KB on desktop computers
