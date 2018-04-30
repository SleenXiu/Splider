# coding=utf-8
# author:xsl
import os, sys
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(CURRENT_DIR, os.pardir)
sys.path.append(PROJECT_DIR)

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
    submit = SubmitField('OK')

class LoginForm(FlaskForm):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

class CreateSourceForm(FlaskForm):
    name = StringField(u'名称', validators=[Required()])
    url = StringField(u'地址', validators=[Required()])
    thidrid = StringField(u'外部标识', validators=[])
    desc = StringField(u'描述', validators=[])
    type = SelectField(u'类型', validators=[Required()], choices=[])
    extra = TextField(u'其他', validators=[])
    submit = SubmitField(u'创建')
