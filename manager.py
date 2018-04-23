#!/usr/bin/env python
# coding=utf-8
# author: xsl


import os, sys
from pymongo import ReadPreference

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(PROJECT_DIR, os.pardir)
sys.path.append(PARENT_DIR)
sys.path.append(PROJECT_DIR)

from mongoengine import connect
connect(alias='testdb', db='testdb', host='127.0.0.1:27017')


