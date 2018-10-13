#!/usr/bin/env python
# coding=utf-8
# author: xsl

import requests, json, urllib
import re
import rsa, binascii, base64
from models import *
import manager
import sys
from urllib3.exceptions import *
from requests.exceptions import *
from lxml import etree
import hashlib
import time, datetime
from utils import upload_img, put_nsq
import pymongo

def get_proxy():
    return requests.get("http://116.196.65.230:8088/get/").content

def genearteMD5(str):
    return hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()

def fix_text(some):
    some = ''.join(some)
    some = some.strip()
    return some

class Splider():

    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
        }
        self._init_db()
        
    def _init_db(self):
        client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        db = client.articledb
        self.article = db.article

    def get_html_by_url(self, url):
        response = self.session.get(url, headers=self.headers)
        return response.text

    def download_img(self, url):
        response = self.session.get(url, headers=self.headers)
        content = response.content
        c_type = response.headers['Content-Type']
        return upload_img(content, "", c_type)


    def parse(self, ahtml):
        html = etree.HTML(ahtml)
        
        date = html.xpath('//span[@class="pub-date"]/text()')
        times = ''.join(date)
        times = times.strip()
        
        
        title = html.xpath('//h1/text()')
        title = ''.join(title)
        title = title.strip()
#        print(title)

        author = html.xpath('//a[@class="note-author"]/text()')
        author = ''.join(author)
        author = author.strip()
#        print(author)

        url = html.xpath('//meta[@property="og:url"]/@content')
        url = ''.join(url)
        url = url.strip()
        
        id = re.findall(r'[0-9]*/$', url)
        id = ''.join(id)
        id = id.strip()
        if id.endswith('/'):
            id = id[:-1]
        print(id)
        
        content1 = html.xpath('//div[@id="link-report"]')[0]
        content = etree.tostring(content1,encoding="utf8", pretty_print=True, method="html")
        content = content.decode('utf-8')
#        print(content)

        c = etree.HTML(content)
        images = c.xpath('//img/@src')

        # https://img1.doubanio.com/view/note/l/public/
        h = 'https://img1.doubanio.com/view/note/l/public/'
        myim = []
        for imurl in images:
            u = imurl.split('/')
            u = u[-1]
            imurl2 = h + u
            myurl = self.download_img(imurl2)
            myim.append(myurl)
            time.sleep(1)

        result = {
            "title": title,
            "author": author,
            "url": url,
            "org_id": id,
            "content": content,
            "date": times,
            "images": myim,
            "type": "douban"
        }

        return result

    def save(self, res):
        c = self.article.find_one({"url":res["url"]})
        if c:
            print(c["title"])
            return c["title"]
        c_id = self.article.insert_one(res).inserted_id
        print(c_id)
        return c_id

#sp = Splider()


#f = open('/Users/qmp/Desktop/456.html')
#a_html = f.read()


#res1 = sp.parse(a_html)
#print(res1)
#res = sp.save(res1)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        url = sys.argv[1]
        sp = Splider()
        html = sp.get_html_by_url(url)
        res = sp.parse(html)
        a = sp.save(res)
    else:
        print('need url')
