# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config
from web.app.init import create_app, db
from configparser import ConfigParser

import pathlib
def getFlaskConfig():
    print("Flask config"+str(pathlib.Path().absolute())+"/"+"Config.ini")
    # Read config.ini file
    config_object = ConfigParser()
    config_object.read(str(pathlib.Path().absolute())+"/"+"Config.ini")
    

    # Get the password
    flask = config_object['FLASK']
    
    print("https://"+flask['ip']+":"+flask['port'])
    return flask

def StartWebServer():
    # WARNING: Don't run with debug turned on in production!
    DEBUG = config('DEBUG', default=True)

    # The configuration
    get_config_mode = 'Debug'

    
    app = create_app() 
    Migrate(app, db)

    app.run(host=getFlaskConfig()['ip'], port=getFlaskConfig()['port'],debug=True, threaded=True)
