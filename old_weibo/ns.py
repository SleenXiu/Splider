#!/usr/bin/env python
# coding=utf-8
# author: xsl

import time
import requests
import os
import json
import urllib
import re
import multiprocessing
from multiprocessing import Process, Queue

idd = ''

session = requests.session()    
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
}
def i_get_statuses(url):
    name = re.findall(r'&page=(.*?)&', url)[0]
    name = int(name)
    ns = []
    for i in range(0, 20):
        ns.append(name+i)
    return ns


def get_statuses(url):
    mblogs = []
    print(url)
    resp = session.get(url, headers=headers)
    result = json.loads(resp.content)
    data = result.get('data')
    cards = data.get('cards')
    for card in cards:
        mblog = card.get('mblog')
        mblogs.append(mblog)
    return mblogs

def createq(q):
    base_url = 'http://m.weibo.cn/api/container/getIndex?'
    params = {
        'type': 'uid',
        'value': idd,
        'containerid': '1076031054009064',
        'page': 1,
        'count': 20
    }
    for i in range(0, 500):
        params['page'] = i
        url = base_url + urllib.parse.urlencode(params)
        name = re.findall(r'&page=(.*?)&', url)[0]
        print('写入'+name)
        q.put(url)
#        time.sleep(0.5)

def read_and_down(q):
    while True:
        url = q.get()
        name = re.findall(r'&page=(.*?)&', url)[0]
        print("读取"+name+" pid"+str(os.getpid()))
        blogs = get_statuses(url)
        with open('dd/page'+name+'.json', 'w') as f:
            json.dump(blogs, f) 

if __name__ == '__main__':
    q = Queue()
    createq(q)
    pr = Process(target=read_and_down,args=(q,))
    pr1 = Process(target=read_and_down,args=(q,))
    pr2 = Process(target=read_and_down,args=(q,))
    pr3 = Process(target=read_and_down,args=(q,))
    pr.start()
    pr1.start()
    pr2.start()
    pr3.start()
    pr.join()
    pr1.join()
    pr2.join()
