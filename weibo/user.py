#!/usr/bin/env python
# coding=utf-8
# author: xsl

import requests
import json
import urllib

page = 1200
def user():
    session = requests.session()

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
    }

    url = 'http://m.weibo.cn/api/container/getIndex?type=uid&value=1054009064&containerid=1076031054009064'
    baseurl = 'http://m.weibo.cn/api/container/getIndex?'
    params = {
        'type': 'uid',
        'value': '1054009064',
        'containerid': '1076031054009064',
        'page': 1,
        'count': 20
    }

    sli = 0
    mblogs = []
    for i in range(0, page):
        params['page'] = i
        url = baseurl + urllib.parse.urlencode(params)
        print(url)
        resp = session.get(url)
        result = json.loads(resp.content)
        data = result['data']
        cards = data['cards']

        for card in cards:
            if not card.__contains__('mblog'):
                continue
            mblog = card['mblog']

            ims = []
            if mblog.__contains__('pics'):
                imgs = mblog['pics']
                for im in imgs:
                    ims.append(im['large']['url'])
            text = mblog['text']
            text = text.replace("\"", "'")
            slblog = {
                'slid': sli,
                'text': text,
                'id': mblog['id'],
                'time': mblog['created_at'],
                'ims': ims,
                'screen_name': mblog['user']['screen_name'],
                'userid': mblog['user']['id']
            }
            sli = sli + 1
            mblogs.append(slblog) 

    print(sli)
    f = open('yifa3.json', 'w', encoding='utf-8')
    d = json.dump(mblogs, f)
  
#    d = d.encode('unicode-escape', 'ignore')
#    d = unicode(d, 'utf-8')
#    d = d.decode('utf-8', 'ignore')
    #f.write(str(d))



if __name__ == '__main__':
    user()

