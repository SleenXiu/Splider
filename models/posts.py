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
    id = ObjectIdField(primary_key=True, default=ObjectId)
    user_id = ObjectIdField()
    url = StringField()
    origin_url = StringField()
    author = StringField()
    title = StringField()
    desc = StringField()
    content = StringField()
    images = ListField()
    source_id = StringField()
    create_at = DateTimeField(default=datetime.datetime.now)
    origin_at = DateTimeField()
    extra = DictField()
