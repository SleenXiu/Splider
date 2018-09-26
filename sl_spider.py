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
import time
from utils import upload_img

def get_proxy():
    return requests.get("http://116.196.65.230:8088/get/").content

def genearteMD5(str):
    return hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()
#    # 创建md5对象
#    hl = hashlib.md5()
#
#    # Tips
#    # 此处必须声明encode
#    # 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
#    hl.update(str.encode(encoding='utf-8'))


class Splider():

    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
        }
        

    def get_html_by_url(self, url):
        response = self.session.get(url, headers=self.headers)
# need proxy
# code
        return response.text

    def download_img(self, url):
        response = self.session.get(url, headers=self.headers)
        content = response.content
        print(type(content))
        title = genearteMD5(url)
#        print(title)
        return upload_img(content, "")


sp = Splider()
#url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1537957806&ver=1146&signature=Wyn2HHiPRmFVnB8onb6qqOb*fKcXhkjCmo*deK48v6jYLQAGpMeUGM2P7p44CaaT3DLeqro8cd8CrLz8WWMvpo1d-AHS6B-CXKhMBlkMsvw2gBlME8LZmtqPvwRWkjRs&new=1'
#
#url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1537957806&ver=1146&signature=Fcog4CJi-a3i-mHBPPmgoT3YbnaAFviIq6T3yoM8qzNADPAOLg*BxGOekZYDDOlnapX2fYkD81sHSRDlBKBDS*BO-8QJqHtpcUlrbsy5AwA5LRE6vy4tE-3vyIwOQ9*G&new=1'
#
#a_html = sp.get_html_by_url(url)

f = open('/Users/qmp/Desktop/345.html')
a_html = f.read()
#print(a_html)

def fix_text(some):
    some = ''.join(some)
    some = some.strip()
    return some


def fix_html(html):
    html = etree.HTML(html)
#    print(html)

    title = html.xpath('//title/text()')
    title = ''.join(title)
    title = title.strip()
    print(title)

    author = html.xpath('//span[@id="js_author_name"]/text()')
    author = ''.join(author)
    author = author.strip()
    print(author)

    wx_name = html.xpath('//a[@id="js_name"]/text()')
    wx_name = fix_text(wx_name)
    print(wx_name)

    meta_content = html.xpath('//div[@id="meta_content"]')
    if len(meta_content) > 0:
        meta_content = meta_content[0]
        author2 = meta_content.xpath('./span[contains(@class, "rich_media_meta_text")]//text()')
        author2 = fix_text(author2)
        author2 = author2.replace(' ','')
        author2 = author2.replace('\n','')
        print(author2)

    wx_info = html.xpath('//div[@class="profile_inner"]/p[@class="profile_meta"]')

    info1 = wx_info[0]
    info_title = info1.xpath('./label/text()')
    info_title = fix_text(info_title)

    info_value = info1.xpath('./span/text()')
    info_value = fix_text(info_value)

    print(info_title+": "+info_value)

    info1 = wx_info[1]
    info_title = info1.xpath('./label/text()')
    info_title = fix_text(info_title)

    info_value = info1.xpath('./span/text()')
    info_value = fix_text(info_value)

    print(info_title+": "+info_value)

    content1 = html.xpath('//div[@id="js_content"]')[0]

    content = etree.tostring(content1,encoding="utf8", pretty_print=True, method="html")
    content = content.decode('utf-8')
    content = re.sub(r' style=\"(.*?)\"', "", content)
#    print(content)

    images = html.xpath('//img/@data-src')
    print(images)

    myim = []
    for url in images:
        myurl = sp.download_img(url)
        myim.append(myurl)
        time.sleep(0.5)

    print(myim)
    i = 0
    for url in images:
        mu = myim[i]
        url = "data-src=\"" + url + "\""
        mu = "src=\"" + mu + "\""
        content = content.replace(url, mu)
        i = i + 1

    print(content)

    content = "<html><head></head><body>"+content+"</body></html>"

    with open("aa.html", 'w') as f:
        f.write(content)



fix_html(a_html)

