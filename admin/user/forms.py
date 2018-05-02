# coding=utf-8
# author:xsl

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField,TextField
from wtforms.validators import Required, Length, DataRequired
from wtforms import ValidationError
import manager

class CreateUserForm(FlaskForm):
    name = StringField('name')
    avatar = StringField('avatar')
    third_id = StringField()
    third_type = StringField()
    extra = StringField()
    email = StringField()
    password = StringField()
    phone = StringField()
    type = StringField()
    submit = SubmitField('Create')

class EditUserForm(FlaskForm):
    name = StringField(u'name')
    avatar = StringField(u'avatar')
    type = StringField(u'type')
    email = StringField(u'email')
    password = StringField(u'password')
    phone = StringField(u'phone')
    submit = SubmitField('OK')


