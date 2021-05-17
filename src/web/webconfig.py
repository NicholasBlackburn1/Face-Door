# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   decouple import config

class Config(object):

    basedir    = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # This will create a file in <app> FOLDER
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
  # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config( 'DB_ENGINE'   , default='postgresql'    ),
        config( 'DB_USERNAME' , default='1234'       ),
        config( 'DB_PASS'     , default='1234'          ),
        config( 'DB_HOST'     , default='172.17.0.3'     ),
        config( 'DB_PORT'     , default=5432            ),
        config( 'DB_NAME'     , default='secuserve' )
    )
class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config( 'DB_ENGINE'   , default='postgresql'    ),
        config( 'DB_USERNAME' , default='1234'       ),
        config( 'DB_PASS'     , default='1234'          ),
        config( 'DB_HOST'     , default='172.17.0.3'     ),
        config( 'DB_PORT'     , default=5432            ),
        config( 'DB_NAME'     , default='secuserve' )
    )

class DebugConfig(Config):
    DEBUG = False

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : ProductionConfig
}
