# coding:utf-8
# author=xls

from mongoengine import connect
db = 'testdb'
host = 'mongodb://127.0.0.1:27017/testdb'
connect(alias=db, host=host)

class App(object):
    def __init__(self):
        self.context = dict({})
        self.debug = true

    def run(self):
        pass
