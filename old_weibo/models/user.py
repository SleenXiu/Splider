#!/usr/bin/env python
# coding=utf-8
# author: xsl

class User():
    def __init__(self):
        pass

    @classmethod
    def new_user(cls, obj):
        user = cls()
        for key in obj:
            value = obj[key]
            setattr(user, key, value)
        return user


