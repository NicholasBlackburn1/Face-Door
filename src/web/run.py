# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config
from app import create_app, db
from configparser import ConfigParser
import webconfig


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


# WARNING: Don't run with debug turned on in production!
try:
    DEBUG = config('DEBUG', default=True)
    get_config_mode = 'Debug' if DEBUG else 'Production'
    # Load all possible configurations
    config_dict = {
        'Production': webconfig.ProductionConfig,
        'Debug'     : webconfig.DebugConfig
    }

    # Load the configuration using the default values
    app_config =config_dict[get_config_mode]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app( app_config ) 
Migrate(app, db)

app.run(host=getFlaskConfig()['ip'], port=getFlaskConfig()['port'],debug=True, threaded=True)
