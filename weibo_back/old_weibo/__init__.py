#!/usr/bin/env python
# coding=utf-8
# author: xsl

import json
from .login import login
from .search import search
from .status import get_statuses_by_user
from .models import User, Status

def test():
    
    f = open("account.json", "r")
    data = f.read()
    data = json.loads(data)
    account = data['weibo']
    res = login(account['account'], account['password'])
    if res:
        print('login successs')

def get_statuses_with_name(name):
    
    u = search(name)
    if u is None:
        print("search user Error")
        return
    print("user is " + u.screen_name)

    page = int(u.statuses_count / 20)

    blogs = get_statuses_by_user(u.id, page)
    
    with open(name+'.json', 'w') as f:
        json.dump(blogs, f)
    
    print(name+"have" +  str(len(blogs)) + "blogs")

def main():
    name = input("weibo name:")
    get_statuses_with_name(name)


if __name__ == "__main__":
    start()
