# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""


import logging
from logging import log
from sys import version
from flask import json
from flask.app import Flask
from flask.helpers import send_from_directory


from flask import jsonify, render_template, redirect, request, url_for
from flask import current_app as app
from flask_login import current_user, login_required, login_user, logout_user

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User
from app.base.util import verify_pass

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

from run import socketio
import run

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

context = zmq.Context()

client = context.socket(zmq.SUB)
client.setsockopt_string(zmq.SUBSCRIBE, "")
client.connect("tcp://127.0.0.1:5000")
authpeople = None

STATIC_FOLDER = "/mnt/user"




@blueprint.route("/")
def route_default():
    return redirect(url_for("base_blueprint.login"))

@socketio.on('connect')
def on_create(data):
    run.logging.info('Created Create event ran\n', data['size'])
    
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


@blueprint.route("/index", methods=["GET", "POST"])
def index():

    return render_template(
        "index.html",
    )


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
