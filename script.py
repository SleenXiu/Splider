# coding=utf-8
# author=xsl

import manager

from models import *

def fix_source_by_user():
    users = User.objects()
    for user in users:
        if user.type != 'weibo':
            continue
        s = Source.objects(thirdid=user.third_id).first()
        if s is None:
            s = Source()
            s.name = user.name
            s.thirdid = user.third_id
            s.type = user.type
            s.url = "https://weibo.com/u/"+user.third_id
            s.save()

