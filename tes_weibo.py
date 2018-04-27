# coding=utf-8
# author:xsl

import manager
from models import *
import re
from weibo import WeiboSplider

s = Source.objects().first()
#url = re.sub(r"//(.*?)/",'//m.weibo.cn/', s.url)
#print(url)

idf = s.thirdid
print(idf)

sp = WeiboSplider()

s_u = sp.search_user('陈一发儿')
if s_u is not None:
    for key in s_u.keys:
        print(key)
#u = User()
#   u.name = s_u.get('screen_name')
#    u.id = s_u.get('id')
#    print(str(u.get('id')))

