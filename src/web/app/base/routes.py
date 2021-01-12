# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
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
from app.base.forms import LoginForm, CreateAccountForm,AddFaceForm,RemoveFaceForm,ServerSettings,ZmqServerSettings
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

print( str(pathlib.Path().absolute())+"/src/web/"+"Config.ini")
# Read config.ini file
config_object = ConfigParser()
config_object.read(str(pathlib.Path().absolute())+"/"+"Config.ini")

logconfig = config_object['LOG']
zmqconfig = config_object['ZMQ']    
flaskconfig = config_object['FLASK']
versionconfig = config_object['VERSION']
settingsconfig = config_object['AMOUNT']
   


'''
TODO: add Reading From Config.ini for Configuring ip and port of flask and more!
'''
# image = client.recv_pyobj()
# unigue_people ->  Unique People Spotted box
# uniquespotted -> presentage og Unique

# authorized -> displayed in the box
# authpre -> presentage of authorizes people

# unknown ->  displayes uknown people in box
# unknown pre ->  presentage of unknown people seen

# errors -> displayes errors accrued
# unotherized displays data in graph

# group -> group displays data from group
# date -. Displays the Current date on the webpage

# Notfication1 =for notitication one tile
# Notification1_data = data for notification 2

# Notification2 = title for notification 2
# Notification2_data= data for notification 2

# Notification3= title for notifcation 3
# Notifcation3_data= data for notifcation3

# Notifcation4 data for title
# Notification4_data for

# Temp -. display for tempature coard
# temppre -> the temp presentage

# uptime -> time that raspi is on uptime
# cpuload -> displays cpu useage dat a
# cpulpre -> cpu useage present

# ownerimg - > displays current image taken of owners from opencv
# parentimg -> displase image of parent taken from fopencv
# unknownimgs

logging.basicConfig(
    filename=logconfig['name'],
    level=logging.DEBUG,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)

zmq_ip = str("tcp://"+zmqconfig['ip']+":"+zmqconfig['port'])
context = zmq.Context()

client = context.socket(zmq.SUB)
client.setsockopt_string(zmq.SUBSCRIBE, "")
client.connect(zmq_ip)
authpeople = None

STATIC_FOLDER = "/mnt/user"


@blueprint.route("/")
def route_default():
    return redirect(url_for("base_blueprint.login"))


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


@blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("base_blueprint.login"))


@blueprint.route("/shutdown")
def shutdown():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")

    return "Server shutting down..."

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template("errors/403.html"), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template("errors/403.html"), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template("page-404.html"), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html"), 500


@blueprint.route("/index", methods=["GET", "POST"])
def index():
    starter = client.recv_string()
    message = client.recv_json()
    
    
    return render_template(
        "index.html",
        unique_people = DataSub.Data.getTotalSeen(starter,message),
        authorized = DataSub.Data.getOwnerPeople(starter,message),
        unknown = DataSub.Data.getUnknownPeople(starter,message),
        ownerimg  =DataSub.Data.getImageFrame(starter,message),
        parentimg=DataSub.Data.getParentImageFrame(starter,message),
        unknownimg=DataSub.Data.getUnknownImageFrame(starter,message),
        version = versionconfig['number'],
        cpuload= psutil.cpu_percent(),
        Ram=psutil.virtual_memory().percent,
        uptime=datetime.now().strftime("%H:%M:%S")
    )   



    
'''
TODO: need to Read from a temp dir for flask to send images from upload dir to Opencv proessing client and save them to opencv local dir  
'''
@blueprint.route("/addFace",methods=["GET", "POST"])
def adduser():
 
    face_from = AddFaceForm(request.form)
    if "add" in request.form:
       
        # read form data
        username = request.form["user"]
        group = request.form["group"]
        
        file = request.files["files"]
        imagename= request.files['files'].filename
        
        tempfile_path= str(pathlib.Path().absolute())+'/src/web/app/base/static/assets/tmp/'
        
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
        print("zmq")
        print(ipaddress)
        print(port)
        
        #Get the configparser object
        config_object = ConfigParser()
        config_object.read(str(pathlib.Path().absolute())+"/src/web/"+"Config.ini")

        zmqsettings = config_object['ZMQ']
        zmqsettings['ip'] = ipaddress
        zmqsettings['port'] = port

        #Write changes back to file
        with open(str(pathlib.Path().absolute())+"/src/web/"+"Config.ini", 'w') as conf:
            config_object.write(conf)
            
        return render_template("settings.html",form = face_from, serverForm= server_form, zmqForm = zmq_form, msg = "updatedzmq",version = versionconfig['number'] )
        
        
        

    
    return render_template("settings.html",form = face_from, serverForm= server_form, zmqForm = zmq_form, version = versionconfig['number'], port_number= flaskconfig['port'], ip_address= flaskconfig['ip'])
    