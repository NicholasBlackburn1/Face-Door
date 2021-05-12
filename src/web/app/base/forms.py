# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField,SelectField
from wtforms.fields.simple import FileField,SubmitField
from wtforms.validators import InputRequired, Email, DataRequired

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

## login and registration

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username_create' , validators=[DataRequired()])
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])


class AddFaceForm(FlaskForm):
    phone = TextField('PhoneNumber', id='phone'   , validators=[DataRequired()])
    user = TextField('name', id='name'   , validators=[DataRequired()])
    files = FileField('files', id='files', validators=[DataRequired()] )
    group = SelectField('group', id='drop', validators=[DataRequired()],choices=[
            ('Admin', 'admin'),
            ('User', 'user'),
            ('Unwanted', 'unwanted')
        ]
    )

    # enables removal of a database entry from the webpage
class RemoveFaceForm(FlaskForm):
    user = TextField('name', id='name'   , validators=[DataRequired()])
    check = SubmitField('files', id='files', validators=[DataRequired()] )
    group = SelectField('group', id='drop', validators=[DataRequired()],choices=[
            ('Admin', 'admin'),
            ('User', 'user'),
            ('Unwanted', 'unwanted')
        ]
    )
    
    
class ServerSettings(FlaskForm):
    ipaddress = TextField('ipaddress ', id='ipaddress'   , validators=[DataRequired()])
    portnumber =  TextField('portnumber ', id='portnumber'   , validators=[DataRequired()])
    

    
class ZmqServerSettings(FlaskForm):
    ipaddress = TextField('ipaddress ', id='ipaddress'   , validators=[DataRequired()])
    portnumber =  TextField('portnumber ', id='portnumber'   , validators=[DataRequired()])
    

    
class AlertPhoneNumberSettings(FlaskForm):
    phonenumber = TextField('phonenumber', id='phonenumber'   , validators=[DataRequired()])
    name = TextField('Name ', id='name'   , validators=[DataRequired()])