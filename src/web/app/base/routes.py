# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us

TODO: add Live camera Displays and minize Non Nessiary data output to main page 
"""


import pathlib
from sys import version

import flask
from werkzeug.utils import cached_property, secure_filename


from zmq.sugar.frame import Message

from flask import json
from flask.app import Flask
from flask.helpers import send_from_directory

from flask import jsonify, render_template, redirect, request, url_for
from flask import current_app as app
from flask_login import current_user, login_required, login_user, logout_user

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm,AddFaceForm,RemoveFaceForm,ServerSettings,ZmqServerSettings,AlertPhoneNumberSettings
from app.base.models import User,Face
from app.base.util import verify_pass
import queue
import zmq
import os
from shutil import copyfile
import psutil
from datetime import datetime, timedelta
from datetime import timedelta
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import yaml
import uuid

import DataSub
import threading
import time 
import socket
import logging

from flask_wtf.file import FileField
from configparser import ConfigParser
# returns the zmq settings from the config.ini

print( str(pathlib.Path().absolute())+"/"+"Config.ini")
# Read config.ini file
config_object = ConfigParser()
config_object.read(str(pathlib.Path().absolute())+"/"+"Config.ini")

logconfig = config_object['LOG']
zmqconfig = config_object['ZMQ']    
flaskconfig = config_object['FLASK']
versionconfig = config_object['VERSION']
settingsconfig = config_object['AMOUNT']
fileconfig = config_object['FILE']
   



'''
TODO: add Reading From Config.ini for Configuring ip and port of flask and more!
'''

logging.basicConfig(
    filename=logconfig['name'],
    level=logging.DEBUG,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)
authpeople = None

STATIC_FOLDER = "/mnt/user"



@blueprint.route("/error-<error>")
def route_errors(error):
    return render_template("errors/{}.html".format(error))


## Login & Registration


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(request.form)
    if "login" in request.form:

        # read form data
        username = request.form["username"]
        password = request.form["password"]

        # Locate user
        user = User.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for("base_blueprint.route_default"))

        # Something (user or pass) is not ok
        return render_template(
            "accounts/login.html", msg="Wrong user or password", form=login_form
        )

    if not current_user.is_authenticated:
        return render_template("accounts/login.html", form=login_form)
    return redirect(url_for("home_blueprint.index"))


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if "register" in request.form:

        username = request.form["username"]
        email = request.form["email"]

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template(
                "accounts/register.html",
                msg="Username already registered",
                success=False,
                form=create_account_form,
            )

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template(
                "accounts/register.html",
                msg="Email already registered",
                success=False,
                form=create_account_form,
            )

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template(
            "accounts/register.html",
            msg='User created please <a href="/login">login</a>',
            success=True,
            form=create_account_form,
        )

    else:
        return render_template("accounts/register.html", form=create_account_form)


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template("errors/403.html"), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template("page-404.html"), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html"), 500


'''
TODO: Get People Seen and reconized to be Read and cal amout of people seen
'''
@blueprint.route("/", methods=["GET", "POST"])
def index():

    
    return render_template(
        "index.html",
        lifetime_people= "Not imp",
        platestotal= "",
    )   



    
@blueprint.route("/addFace",methods=["GET", "POST"])
def adduser():
 
    face_from = AddFaceForm(request.form)
    if "add" in request.form:
       
        # read form data
        username = request.form["user"]
        group = request.form["group"]
        
        file = request.files["files"]
        imagename= request.files['files'].filename
        
        tempfile_path= str(pathlib.Path().absolute())+'/app/base/static/assets/tmp/'
        
        output_name = str(uuid.uuid1())+".jpg"
        
        tempfile_url = str('http://'+flaskconfig['ip']+':'+flaskconfig['port']+"/static/assets/tmp/"+output_name)
        

        print(username)
        print(group)
        print(imagename)
        print(tempfile_url)
        
        # saves uploaded image to a temp file dir for sending to opencv client 
        file.save(tempfile_path+output_name)

        # Check usename exists
        user = Face.query.filter_by(user=username).first()
        if user:
            return render_template(
                 "addFace.html",
                msg="Username already registered",
                success=False,
                form= face_from,
            )

        # Check email exists
        user = Face.query.filter_by(group=group).first()
        
      
        user = Face.query.filter_by(image="none")
      
        
        
        user = Face(**request.form)
        user.image = output_name
        user.imageurl = tempfile_url
        user.useruuid = str(uuid.uuid1())
        db.session.add(user)
        db.session.commit()
        ##print(image)

        
    return render_template("addFace.html",form = face_from)

# Renders and handles the settings of the backend server
@blueprint.route("/settings",methods=["GET", "POST"])
def settings():

  
    
    face_from = RemoveFaceForm(request.form)
    server_form = ServerSettings(request.form)
    zmq_form = ZmqServerSettings(request.form)
    phone_form = AlertPhoneNumberSettings(request.form)
    
    if "Remove" in request.form:
        username = request.form['user']
        group = request.form['group']

        print(username)
        print(group)

        remove = Face.query.filter_by(user=username).one()
        db.session.delete(remove)
        db.session.commit()
              
        return render_template("settings.html",form = face_from, serverForm= server_form, zmqForm = zmq_form, msg = "removedUser" )
        
    if "save" in request.form:
        ipaddress = request.form['ipaddress']
        port = request.form['portnumber']
        
        print(ipaddress)
        print(port)
        
        #Get the configparser object
       
        #Get the configparser object
        config_object = ConfigParser()
        config_object.read(str(pathlib.Path().absolute())+"/src/web/"+"Config.ini")

        flasksettings = config_object['FLASK']
        flasksettings['ip'] = ipaddress
        flasksettings['port'] = port
        
        #Write changes back to file
        with open(str(pathlib.Path().absolute())+"/src/web/"+"Config.ini", 'w') as conf:
            config_object.write(conf)
        return render_template("settings.html",form = face_from, serverForm= server_form, zmqForm = zmq_form, msg = "updated",version = versionconfig['number'] )
        

    if "zmqsave" in request.form:
        
        ipaddress = request.form['ipaddress']
        port = request.form['portnumber']
        print("ZMQ")
        print(ipaddress)
        print(port)
        
        #Get the configparser object
        config_object = ConfigParser()
        config_object.read(str(pathlib.Path().absolute())+"/src/web/"+"Config.ini")

        zmqsettings = config_object['ZMQ']
        zmqsettings['ip'] = ipaddress
        zmqsettings['port'] = port

    if "phonesave" in request.form:
        phone = request.form['phonenumber']
        usrname = request.form['name']
        data = {    
            "name": usrname,
            "phonenum": phone,
            }

        #Write changes back to file
        with open(fileconfig['rootDirPath']+fileconfig['configPath']+fileconfig['PhoneNumberStorage']+"PhoneNumber.json", 'w') as conf:
            json.dump(data,conf)
            
        return render_template("settings.html",form = face_from, serverForm= server_form, zmqForm = zmq_form, phoneForm = phone_form, msg = "addedphone",version = versionconfig['number'] )
        
        
        

    
    return render_template("settings.html",form = face_from, serverForm= server_form, zmqForm = zmq_form,  phoneForm = phone_form, version = versionconfig['number'], port_number= flaskconfig['port'], ip_address= flaskconfig['ip'])
    