# homoiconic programming in models {#homo}

* https://ponyatov.quora.com/
	* [Model-Driven Venture](https://ponyatov.quora.com/Model-Driven-Venture)
	  on replacing Model-Driven Development with **homoiconic programming in models**

Every time I try to read something about MDA, I see nifty presentations with an 
advertisement for a million-dollars commercial system with UML-like 
mouse-dragging interface, but **in result this system able to produce only 
database schema and a class-definitions skeleton** with getters and barking 
setters, without any code implements things the resulting application must do. 
(maybe something changed from the time when I play with a few demos)

**To make the technology alive, it should be built on** 
* executable semantics, 
* metaprogramming, and 
* self-modification from the ground bare-metal level.
 
Something with the feel of Lisp in the heart but not so mindblowing recursion 
and more human-friendly syntax. A lot of things programmer must be able to do:
* model transformation by execution of models describes these transformations, 
  **sort of homoiconic computation** defined in the modeling domain
* generic programming in terms of abstract models widely used in software 
development (class and object relations, database schemas, data flow, 
finite automata, algorithm definitions, generic hardware descriptions, etc)
* rich and powerful but easy to use code generators into any programming, 
build control and DML/DDL languages
* knowledge base + expert system, with fuzzy search, contains a lot of 
parametric code snippets, and symbolic/logic computation mechanics lets to 
match these code snippets with models you are working with

**Making code from mouse-drafted diagrams is the dead idea by design**, look 
say on LabView, it's the maybe only thing someone can say it works. 
Convert these multilayer nested diagrams into some DSL code — oops, 
this is the only single page of fully observable code in place of hours 
of mouse swanking.

But the reverse case can be really usable: visualize code (or models) 
buy your scripts, and every diagram not only shows your thinking, but plays 
a role of test — if you made something wrong in code/model, you get oddities 
in the draw, or repaint will be broken in a whole.