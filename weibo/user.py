#!/usr/bin/env python
# coding=utf-8
# author: xsl

import requests
import json

def user():
    session = requests.session()

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
    }

    url = 'http://m.weibo.cn/api/container/getIndex?type=uid&value=1054009064&containerid=1076031054009064'

    resp = session.get(url)

    result = json.loads(resp.content)

    data = result['data']
    cards = data["cards"]

    mblogs = []
    for card in cards:
        if not card.__contains__('mblog'):
            continue
        mblog = card['mblog']
        
        ims = []
        if mblog.__contains__('pics'):
            imgs = mblog['pics']
            for im in imgs:
                ims.append(im['large']['url'])
        
        slblog = {
            'text': mblog['text'],
            'id': mblog['id'],
            'time': mblog['created_at'],
            'ims': ims,
            'screen_name': mblog['user']['screen_name']
        }
        mblogs.append(slblog)

    print(mblogs)


if __name__ == '__main__':
    user()
