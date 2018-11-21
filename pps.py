## @file
## @brief Personal Planning System

from sym import *

## @defgroup pps PPS
## @brief Personal Planning System
## @{

class Plan(Object):
    def push(self,obj): self[obj.value] = obj ; return self

## activity task
class Task(Plan): pass

## procrastination
class Frog(Task): pass

## supertask must be splitted
class Eleph(Task): pass

## target axes (metrics)
class Axis(Plan): pass

## sheduler
class Shed(Plan): pass

## @}
