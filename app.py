# coding:utf-8
# author=xls
import os, sys

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(PROJECT_DIR, os.pardir)
sys.path.append(PARENT_DIR)
sys.path.append(PROJECT_DIR)

from mongoengine import connect
db = 'testdb'
host = 'mongodb://127.0.0.1:27017/testdb'
connect(alias='testdb', db='testdb', host='127.0.0.1:27017')

from models import User


class App(object):
    def __init__(self):
        self.context = dict({})
        self.debug = True

    def run(self):
        pass
