## @file

import os,sys

## @defgroup web Web interface
## @brief Flask powered
## @{

,flask_wtf,wtforms

## IP addr to bind 

## IP port to bind

## debug mode must be enabled only on dev station
DEBUG = False

## Flask application



## @defgroup auth authorization
## @brief HTTPS and hashed login/password for single user only
## @{

import flask_login

## login manager
logman = flask_login.LoginManager() ; logman.init_app(app)

# this module can't be publicated on github
from secrets import LOGIN_HASH, PSWD_HASH, SSL_KEYS

try:
    # check files available
    for i in SSL_KEYS: open(i,'r').close()
except IOError:
    SSL_KEYS = None
    # force only local bind, does not put your ass to Internet or even LAN
    IP = '127.0.0.1'
    # enable debug on dev station
    DEBUG = True
    
## @}

## @}
