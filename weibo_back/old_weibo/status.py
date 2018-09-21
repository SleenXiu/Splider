#!/usr/bin/env python
# coding=utf-8
# author: xsl

import requests
import json
import urllib
import re
import ssl
from .models import Status

ssl._create_default_https_context = ssl._create_unverified_context

def get_statuses_by_user(userid, maxpage=10):
    
    base_url = 'http://m.weibo.cn/api/container/getIndex?'
    session = requests.session()
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
    }
    params = {
        'type': 'uid',
        'value': userid,
        'containerid': '1076031054009064',
        'page': 1,
        'count': 20
    }
    
    sl_id = 0
    mblogs = []
    for i in range(0, maxpage):
        params['page'] = i
        url = base_url + urllib.parse.urlencode(params)
        print(url)
        resp = session.get(url, headers=headers)
        result = json.loads(resp.content)
        data = result['data']
        cards = data['cards']
        
        for card in cards:
            if card.__contains__('mblog'):
                mblogs.append(card['mblog'])

    print(mblogs)
    return mblogs

def get_status_by_id(status_id):
    url = 'https://m.weibo.cn/status/' + status_id
    print(url)
    session = requests.session()
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
    }
    resp = session.get(url, headers=headers, verify=False, timeout=60)
    result = resp.text
    data = re.findall(r'render_data = ([\s\S]*?)\[0\] \|\| \{\};', result)
    obj = json.loads(data[0])
    return obj

def haha():
    ids = 'G9t2tx95G'
    data = get_status_by_id(ids)
    status = Status.new_status(data[0]['status'])
    return status

if __name__ == '__main__':
#data = get_statuses_by_user('1054009064', maxpage=1)
#    with open('tmp.json', 'w') as f:
#        json.dump(data, f)
    ssl._create_default_https_context = ssl._create_unverified_context
    ids = '4184796936152222'
    ids = 'G9t2tx95G'
    data = get_status_by_id(ids)
    status = Status.new_status(data[0]['status'])
    print(status.id)
#with open(ids+'.json', 'w') as f:
#       json.dump(data, f)
