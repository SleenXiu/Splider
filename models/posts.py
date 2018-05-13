# coding=utf-8
# author:xsl
import datetime
from bson import ObjectId
from mongoengine import (
        StringField,
        Document,
        IntField,
        BooleanField,
        ObjectIdField,
        ListField,
        DictField,
        DateTimeField,
        )

class Post(Document):
    meta = {
        'db_alias': 'testdb',
        'index_background': True,
        'indexes': [
        ],
    }
    id = ObjectIdField(primary_key=True, default=ObjectId)
    user_id = ObjectIdField()
    url = StringField()
    origin_url = StringField()
    origin_id = StringField()
    origin_at = DateTimeField()
    author = StringField()
    author_id = StringField()
    text = StringField()
    title = StringField()
    desc = StringField()
    content = StringField()
    images = ListField()
    source_id = StringField()
    create_at = DateTimeField(default=datetime.datetime.now)
    extra = DictField()

class Weibo(Document):
    meta = {
        'db_alias': 'testdb',
        'index_background': True,
        'indexes': [
        ],
    }

    id = ObjectIdField(primary_key=True, default=ObjectId)
    x_create_at = DateTimeField(default=datetime.datetime.now)
    org_id = IntField()
    extra = DictField()
