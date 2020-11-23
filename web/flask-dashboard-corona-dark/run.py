# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

import logging
from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config
from flask_socketio import SocketIO

from config import config_dict
from app import create_app, db
from flask_socketio import SocketIO, emit

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'
# unknownimgs



try:
    
    # Load the configuration using the default values 
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app( app_config ) 
Migrate(app, db)
socketio = SocketIO(app)


handler = logging.FileHandler("test.log")  # Create the file logger
app.logger.addHandler(handler)             # Add it to the built-in logger
app.logger.setLevel(logging.DEBUG) 
app.logger.info('hello')   
if __name__ == "__main__":
      
    app.config['SECRET_KEY'] = 'secret!'
    socketio.run(app,host='127.0.0.1', port=2000)