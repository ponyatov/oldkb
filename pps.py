## @file
## @brief Personal Planning System

from sym import *

## @defgroup pps PPS
## @brief Personal Planning System
## @{

class Plan(Object): pass

## activity task
class Task(Plan): pass

## target axes (metrics)
class Axes(Plan): pass

## sheduler
class Shed(Plan): pass

## @}
