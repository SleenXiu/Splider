# coding=utf-8
# author:xsl

from flask import Blueprint

user = Blueprint('user', __name__)

from . import views