# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField,SelectField
from wtforms.fields.simple import FileField
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
    user = TextField('name', id='name'   , validators=[DataRequired()])
  
    group = SelectField('group', id='drop', validators=[DataRequired()],choices=[
            ('Admin', 'admin'),
            ('User', 'user'),
            ('Unwanted', 'unwanted')
        ]
    )
    