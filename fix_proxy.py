# coding=utf-8
# author:xsl

import requests
from urllib3.exceptions import *
from requests.exceptions import *
import sys

def get_proxy():
    return requests.get("http://116.196.65.230:8088/get/").content


def delete_proxy(proxy):
    url = "http://116.196.65.230:8088/delete/?proxy="+proxy
    return requests.get(url)


session = requests.session()
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
}

ok = []

def fix_proxy():
    url = 'http://ip.cn'
    proxy = get_proxy().decode("utf8")
        # self.session.proxies = {'http': 'http://{}'.format(proxy)}
    print(proxy)
    proxies = {'http': 'http://{}'.format(proxy),'https': 'http://{}'.format(proxy)}
    print(proxies)
    session.proxies = proxies
    try:
        resp = session.get(url, verify=False, timeout=2)
        return proxy
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

    delete_proxy(proxy)
    return None

import time



while (1):
    time.sleep(0.5)
    a = fix_proxy()
    if a:
        print("ok:"+a)
