## @file
## @brief Personal Planning System

from sym import *

## @defgroup pps PPS
## @brief Personal Planning System
## @{

class Plan(Object): pass
    
## target axes (metrics)
class Axis(Plan): pass

## sheduler
class Shed(Plan): pass

## @defgroup task task
## @{

## activity task
class Task(Plan): pass

## periodic task
class Regular(Task): pass

## alarm must be activated in precision time
class Alarm(Task): pass

## procrastination point
class Frog(Task): pass

## supertask must be splitted
class Slon(Task): pass

## @}

## @defgroup geo geolocation
## @{

## geolocation
class Place(Plan): pass

## @}

## @defgroup contact contacts
## @brief & HR
## @{

## contact
class Contact(Plan): pass

## telephone
class Tel(Contact): pass

## @}

## @}
