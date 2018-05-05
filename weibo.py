#!/usr/bin/env python
# coding=utf-8
# author: xsl

import requests, json, urllib
import re
import rsa, binascii, base64
from weibo_config import Config


class WeiboSplider():

    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-cn',
            "Accept-Encoding": "gzip, deflate, br",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
        }
        

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

    def get_weiboes_by_userid(self, userid, count):
        # need multiprocessing        
        pass        

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

def testGet():
    id = '1054009064'

if __name__ == "__main__":
    #testLogin()
    testSearch()
