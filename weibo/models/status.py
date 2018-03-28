#!/usr/bin/env python
# coding=utf-8
# author: xsl

from . import User

class Status():

    def __init__(self):
        pass

    @classmethod
    def new_status(cls, obj):
        status = cls()
        for key in obj:
            value = obj[key]
            if key == 'user':
                value = User.new_user(value)
            setattr(status, key, value)
        return status

class Pic():
    
    def __init__(self):
        pass
