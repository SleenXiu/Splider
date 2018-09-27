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
from utils import upload_img
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
        db = client.wechatdb
        self.db_contents = db.content

    def get_html_by_url(self, url):
        response = self.session.get(url, headers=self.headers)
        return response.text

    def download_img(self, url):
        response = self.session.get(url, headers=self.headers)
        content = response.content
        return upload_img(content, "")


    def parse(self, ahtml):
        html = etree.HTML(ahtml)
        
        date = re.findall(r'ct\s*=\s*\"[0-9]*\"', ahtml)
        if len(date) > 0:
            date = date[0]
        date = re.findall(r'\"[0-9]*\"', date)[0]
        date = date[1:-1]
        times = datetime.datetime.fromtimestamp(int(date))
        
        
        title = html.xpath('//title/text()')
        title = ''.join(title)
        title = title.strip()
#        print(title)

        author = html.xpath('//span[@id="js_author_name"]/text()')
        author = ''.join(author)
        author = author.strip()
#        print(author)

        wx_name = html.xpath('//a[@id="js_name"]/text()')
        wx_name = fix_text(wx_name)
#        print(wx_name)

        meta_content = html.xpath('//div[@id="meta_content"]')
        author2 = author
        if len(meta_content) > 0:
            meta_content = meta_content[0]
            author2 = meta_content.xpath('./span[contains(@class, "rich_media_meta_text")]//text()')
            author2 = fix_text(author2)
            author2 = author2.replace(' ','')
            author2 = author2.replace('\n','')
#            print(author2)

        wx_info = html.xpath('//div[@class="profile_inner"]/p[@class="profile_meta"]')

        info1 = wx_info[0]
        info_title = info1.xpath('./label/text()')
        info_title = fix_text(info_title)

        info_value1 = info1.xpath('./span/text()')
        info_value1 = fix_text(info_value1)

#        print(info_title+": "+info_value1)

        info1 = wx_info[1]
        info_title = info1.xpath('./label/text()')
        info_title = fix_text(info_title)

        info_value = info1.xpath('./span/text()')
        info_value = fix_text(info_value)

#        print(info_title+": "+info_value)

        content1 = html.xpath('//div[@id="js_content"]')[0]

        content = etree.tostring(content1,encoding="utf8", pretty_print=True, method="html")
        content = content.decode('utf-8')
        content = re.sub(r' style=\"(.*?)\"', "", content)
            #    print(content)

        images = html.xpath('//img/@data-src')
#        print(images)

        myim = []
        for url in images:
            myurl = self.download_img(url)
            myim.append(myurl)
            time.sleep(1)
            
#        print(myim)
        content1 = content
        i = 0
        for url in images:
            mu = myim[i]
            url = "data-src=\"" + url + "\""
            mu = "src=\"" + mu + "\""
            content1 = content1.replace(url, mu)
            i = i + 1
            
#        print(content1)

        result = {
            "title": title,
            "wx_name": wx_name,
            "wx_author": author,
            "wx_author2": author2,
            "wx_code": info_value1,
            "wx_desc": info_value,
            "wx_images": images,
            "images": myim,
            "wx_content": content,
            "content": content1,
            "wx_time": times
        }

        return result

    def save(self, res):
        c = self.db_contents.find_one({"title":res["title"]})
        if c:
            print(c["title"])
        c_id = self.db_contents.insert_one(res).inserted_id
        print(c_id)

sp = Splider()


f = open('/Users/qmp/Desktop/123.html')
a_html = f.read()


res1 = sp.parse(a_html)
res = sp.save(res1)





