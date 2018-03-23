# coding=utf-8
# Author: sleen


import base64
import urllib
import json
import requests
import rsa
import binascii
import re

def login(username, password):
    pre_url = "http://login.sina.com.cn/sso/prelogin.php"

    su = base64.b64encode(username.encode(encoding="utf-8"))
    pre_param = {
        "entry": "weibo",
        "callback": "sinaSSOController.preloginCallBack",
        "su": su,
        "rsakt": "mod",
        "checkpin": 1,
        "client": "ssologin.js(v1.4.19)",
        "_": "1521133114145"
    }
    pre_data = urllib.parse.urlencode(pre_param)
    pre_url_new = pre_url + "?" + pre_data

    print(pre_url_new)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }

    session = requests.Session()
    pre_resp = session.get(pre_url_new, headers=headers)
    result = pre_resp.text
    pre_result = result[result.find('(')+1:-1]
    pre_data = json.loads(pre_result)
    print (pre_data)

    pubkey = pre_data["pubkey"]
    servertime = pre_data["servertime"]
    nonce = pre_data["nonce"]

    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)
    msg = str(servertime) +'\t' + str(nonce) + '\n' + str(password)
    sp = binascii.b2a_hex(rsa.encrypt(msg.encode("utf-8"), key))

    login_url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)"
    login_param = {
        "entry": "weibo",
        "getway": 1,
        "form": "",
        "savestate": 7,
        'userticket': '1',
        'ssosimplelogin': '1',
        'pwencode': 'rsa2',
        "vsnf": 1,
        'vsnval': '',
        "su": su,
        "sp": sp,
        "service": "miniblog",
        "servertime": pre_data["servertime"],
        "nonce": pre_data["nonce"],
        "rsakv": pre_data["rsakv"],
        "encoding": "UTF-8",
        "url":"https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
        "returntype": "META"
    }

    response = session.post(login_url, data=login_param, headers=headers) 

    text = response.content
    redirect_urls = re.findall(r'https%3A%2F%2Fweibo.*retcode%3D0', response.text)
    if len(redirect_urls) <= 0:
        return False
    redirect_url = redirect_urls[0]
    print(redirect_url)
    redirect_url = urllib.parse.unquote(redirect_url)
    res = session.get(redirect_url)
    print(res.text)

    cookie = json.dumps(session.cookies.get_dict())

    f = open('weibo/cookie.data','w')
    f.write(cookie)
    f.close()

    return True

if __name__ == "__main__":
    username = ""
    password = ""
    login(username, password)











