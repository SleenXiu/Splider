#!/usr/bin/env python
# coding=utf-8
# author: xsl

import os
import json

f = open("cookie.data", "r")
cookie = f.read()
print(cookie)

cookie = json.loads(cookie)

import requests


session = requests.session()

session

requests.utils.add_dict_to_cookiejar(session.cookies, cookie)


str = "https://weibo.com/u/"
res = session.get(str)

dd = res.content

print(dd.decode("utf-8"))

f = open("1.html", "w")
f.write(dd.decode("utf-8"))
f.close()
