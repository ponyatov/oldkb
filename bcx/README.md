# bcx
## BCX: bytecode/FORTH runtime
### for tiny embedded (Cortex-M MCUs)

(c) Dmitry Ponyatov <<dponyatov@gmail.com>> , All rights reserved

github: https://github.com/ponyatov/bcx

manual: https://ponyatov.github.io/bcx

## About

This is bytecode interpreter runtime targeted for really tiny embedded systems
which have a few Kb of RAM: specifically for Cortex-M microcontrollers. The main
goal of this system is providing fully-functional command line console (CLI) for 
embedded devices, to make them interactively controllable by the user, and 
provide readable text API for automation scripts. FORTH programming language 
is still staying ideal model for CLI applications in resource-constrained 
devices, so bcx system shipped both with the assembly-like compiler and small 
FORTH system as default console shell.
