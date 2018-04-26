# coding=utf-8
# author:xsl

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField,TextField
from wtforms.validators import Required, Length, DataRequired
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

class CreateSourceForm(FlaskForm):
    name = StringField(u'名称', validators=[Required()])
    url = StringField(u'地址', validators=[Required()])
    desc = StringField(u'描述', validators=[])
    type = SelectField(u'类型', validators=[Required()], choices=[('0', 'weibo'),('1', 'wechat'),('2', 'zhihu')])
    extra = TextField(u'其他', validators=[])
    submit = SubmitField(u'创建')
