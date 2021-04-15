# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config

from config import config_dict
from app import create_app, db
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

    try:
        
        # Load the configuration using the default values 
        app_config = config_dict[get_config_mode.capitalize()]

    except KeyError:
        exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

    app = create_app( app_config ) 
    Migrate(app, db)

    app.run(host=getFlaskConfig()['ip'], port=getFlaskConfig()['port'],debug=True, threaded=True)
