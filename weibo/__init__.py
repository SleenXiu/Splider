#!/usr/bin/env python
# coding=utf-8
# author: xsl

import json
from .login import login

def start():
    
    f = open("account.json", "r")
    data = f.read()
    data = json.loads(data)
    account = data['weibo']
    res = login(account['account'], account['password'])
    if res:
        print('login successs')


if __name__ == "__main__":
    start()
