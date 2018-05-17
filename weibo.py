#!/usr/bin/env python
# coding=utf-8
# author: xsl

import requests, json, urllib
import re
import rsa, binascii, base64
from weibo_config import Config
from models import *
import manager
import sys
from urllib3.exceptions import *
from requests.exceptions import *

def get_proxy():
    return requests.get("http://116.196.65.230:8088/get/").content


class WeiboSplider():

    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
        }
        self.re_get_proxy()
        

    def login(self, account, password):
        headers = self.headers 
        pre_login_url = "http://login.sina.com.cn/sso/prelogin.php?"
        
        su = base64.b64encode(account.encode(encoding="utf-8"))

        Config.pre_login_params['su'] = su
        pre_params = Config.pre_login_params
        pre_login_url = pre_login_url + urllib.parse.urlencode(pre_params)
        print(pre_login_url)

        response = self.session.get(pre_login_url, headers=headers, verify=False)
        result = response.text[response.text.find('(')+1:-1]
        data = json.loads(result)
        print(data)

        pubkey = data["pubkey"]
        servertime = data["servertime"]
        nonce = data["nonce"]
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)
        msg = str(servertime) +'\t' + str(nonce) + '\n' + str(password)
        sp = binascii.b2a_hex(rsa.encrypt(msg.encode("utf-8"), key))
        
        login_url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)"
        Config.login_params['su'] = su
        Config.login_params['sp'] = sp
        Config.login_params['servertime'] = data["servertime"]
        Config.login_params['nonce'] = data['nonce']
        Config.login_params['rsakv'] = data["rsakv"]
        login_params = Config.login_params

        response = self.session.post(login_url, data=login_params, headers=headers, verify=False)
        redirect_urls = re.findall(r'https%3A%2F%2Fweibo.*retcode%3D0', response.text)
        if len(redirect_urls) <= 0:
            return False

        redirect_url = redirect_urls[0]
        redirect_url = urllib.parse.unquote(redirect_url)
        res = self.session.get(redirect_url)
        cookie = json.dumps(self.session.cookies.get_dict())
        self.cookie = cookie
        return True

    def search_user_list(self, username):
        url = 'https://m.weibo.cn/api/container/getIndex?'
        Config.search_params['queryVal'] = username
        Config.search_params['containerid'] = '100103type=3&q=' + username
        params = urllib.parse.urlencode(Config.search_params)
        url = url + params

        response = self.session.get(url, headers=self.headers, verify=False)
        if response.status_code > 300:
            print('search error:'+ str(response.status_code))
            return None
        data = json.loads(response.text).get('data')
        cards = data.get('cards')
        if len(cards) < 1:
            return None
        card = data.get('cards')[1]
        user_group = card.get('card_group')
        user = user_group[0].get('user')
        return user_group


    def search_user(self, username):
        url = 'https://m.weibo.cn/api/container/getIndex?'
        Config.search_params['queryVal'] = username
        Config.search_params['containerid'] = '100103type=3&q=' + username
        params = urllib.parse.urlencode(Config.search_params)
        url = url + params

        response = self.session.get(url, headers=self.headers, verify=False)
        if response.status_code > 300:
            print('search error:'+ str(response.status_code))
            return None
        data = json.loads(response.text).get('data')
        cards = data.get('cards')
        if len(cards) < 1:
            return None
        card = data.get('cards')[1]
        user_group = card.get('card_group')
        user = user_group[0].get('user')
        return user

    def get_weiboes_by_userid(self, userid):
        base_url = 'http://m.weibo.cn/api/container/getIndex?'
        params = {
            'type': 'uid',
            'value': userid,
            'containerid': '107603'+userid,
            'page': 1,
            'count': 20
        }
        sl_id = 0
        mblogs = []
        maxpage = 200
        for i in range(0, maxpage):
            params['page'] = i
            url = base_url + urllib.parse.urlencode(params)
            print(url)
            resp = self.session.get(url, headers=self.headers)
            result = json.loads(resp.content)
            data = result['data']
            cards = data['cards']

            for card in cards:
                mblog = card.get("mblog")
                blog = self._fixBlog(mblog)
                if blog:
                    blog.save()
                    mblogs.append(blog)

#print(mblogs)
        return mblogs

    def _fixBlog(self, blog):

        print(blog)
        if blog is None:
            return None
        tid = str(blog.get("id"))
        b = Post.objects(origin_id=tid).first()
        if b is None:
            b = Post()
        b.origin_id = str(blog.get("id"))
        b.text = blog.get("text")
# b.origin_at = blog.get("created_at")
        b.origin_url = "https://m.weibo.cn/status/"+b.origin_id
        b.text = blog.get("text")
        b.images = blog.get("pics")
        user = blog.get("user")
        b.author = user.get("screen_name")
        b.author_id = str(user.get("id"))
        return b

    def re_get_proxy(self):
        self.proxy = get_proxy().decode("utf8")

    def get_status_by_id(self, status_id):
        url = 'https://m.weibo.cn/status/' + status_id
        proxy = self.proxy
        proxies = {'http': 'http://{}'.format(proxy),'https': 'http://{}'.format(proxy)}
        self.session.proxies = proxies
        try:
            resp = self.session.get(url, headers=self.headers, verify=False, timeout=2)
            result = resp.text
            data = re.findall(r'render_data = ([\s\S]*?)\[0\] \|\| \{\};', result)
            if len(data) > 0:
                obj = json.loads(data[0])
                if len(obj) > 0:
                    return obj[0]
            else:
                self.re_get_proxy()
                self.get_status_by_id(sratus_id)

        except requests.exceptions.ConnectTimeout:
            self.re_get_proxy()
            self.get_status_by_id(status_id)
            print('timeout')
        except requests.exceptions.ReadTimeout:
            self.re_get_proxy()
            self.get_status_by_id(status_id)
            print('read timeout')
        except HTTPError as e:
            self.re_get_proxy()
            self.get_status_by_id(status_id)
            print(proxy+'fail')
            # delete_proxy(proxy)
        except ReadTimeoutError:
            self.re_get_proxy()
            self.get_status_by_id(status_id)
            print('timeout')
        except ConnectionError:
            self.re_get_proxy()
            self.get_status_by_id(status_id)
            print('ConnectionError')
        except KeyboardInterrupt:
            sys.exit(0)
        
        

    def fix_proxy(self):
        url = 'http://ip.cn'
        proxy = get_proxy().decode("utf8")
        # self.session.proxies = {'http': 'http://{}'.format(proxy)}
        print(proxy)
        proxies = {'http': 'http://{}'.format(proxy),'https': 'http://{}'.format(proxy)}
        print(proxies)
        self.session.proxies = proxies
        try:
            resp = self.session.get(url, verify=False, timeout=2)
            print(resp.text)
        except requests.exceptions.ConnectTimeout:
            print('timeout')
        except requests.exceptions.ReadTimeout:
            print('read timeout')
        except HTTPError as e:
            print(proxy+'fail')
            # delete_proxy(proxy)
        except ReadTimeoutError:
            print('timeout')
        except ConnectionError:
            print('ConnectionError')
        except KeyboardInterrupt:
            sys.exit(0)

sp = WeiboSplider()

def testLogin():
    if (sp.login('', '')):
        print("login success")
        return
    print("login failure")

def testSearch():
    u = sp.search_user('陈一发儿') 
    if u:
        print("find :"+ u.get('screen_name') +"id:"+ str(u.get('id')))
    else:
        print("no find")

def testGet(uid):
    id = '1054009064'
    id = '2331621641'
    id = '1774676624'
    id = "2686948620"
    sp.get_weiboes_by_userid(uid)

def tesetFixStatus():
    id = '4160725867915976'
    s = sp.get_status_by_id(id)
    print(s)

import time
def fixAllWeibo(uid):
    ps = Post.objects(author_id=uid)
    for p in ps:
        print(p.origin_id)
        w = Weibo.objects(org_id=p.origin_id).first()
        if w:
            print('did')
            continue
        s = sp.get_status_by_id(p.origin_id)
        if s is None:
            continue
        w = Weibo()
        status = s.get('status')
        w.org_id = status.get('id')
        w.extra = status #json.dumps(status)
        w.save()

def textProxy():
    for i in range(0, 10):
        sp.fix_proxy()

import sys
if __name__ == "__main__":
    arg = sys.argv[1]
    uid = sys.argv[2]
    print(sys.argv)
    if arg == '1':
        print('start get post')
        testGet(uid)
    elif arg == '2':
        print('start get weibo')
        fixAllWeibo(uid)
    else:
        print('nothing')
    # testLogin()
    # testSearch()
    # testGet()   
    # tesetFixStatus() 
    # fixAllWeibo("2686948620")
    # textProxy()
