# knowledge base {#kb}

@brief object/graph/knowledge database

This @ref kb system primarily targets for hardware & software codesign.

Most software development tightly linked with a lot of programming languages,
which requires 
* configurable syntax parsing for any programming languages
* transforming source code into AST abstract syntax and parse trees representation
* computer-assisted source code traverse and analysis

This like task needs a lot of data input and browsing
in form of deep trees (AST, syntax parse, project files,..) and (hyper)graphs.
That's why pure FORTH is not applicable in practice without a special
@ref ts extension.