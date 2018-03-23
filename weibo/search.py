#!/usr/bin/env python
# coding=utf-8
# author: xsl

import requests
import urllib
import json

def search(username):

    session = requests.session()

    url = 'https://m.weibo.cn/api/container/getIndex?'
    name = username
    param = {
        'type': 'all',
        'queryVal': name,
        'containerid': '100103type=3&q='+name
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
    }

    param_en = urllib.parse.urlencode(param)

    url = url + param_en
    print(url)
    res = session.get(url, headers=headers)

    dd = res.content

    data = json.loads(res.text)

    cards = data['data']['cards']
    users = cards[1]['card_group']
    user = users[0]['user']

    return user


if __name__ == "__main__":
    search()
