#!/usr/bin/env python
# coding=utf-8
# author: xsl

import json

mm = []

ff = open('all.json', 'w')
for i in range(0, 750):
    with open('page'+str(i)+'.json', 'r') as f:
        d = f.read()
        mm.extend(json.loads(d))

print(len(mm))

json.dump(mm, ff)
