#!/usr/bin/env python
# coding=utf-8
# author: xsl

import requests
import json

session = requests.session()
resp = session.get("https://www.baidu.com")

co = json.dumps(session.cookies.get_dict())

#f = open("c.data", "w")

#f.write(co)


print(co)

f = open("c.data", "r")

s = f.read()

print (s)

session.cookies.set(s)
