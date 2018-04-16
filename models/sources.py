# coding=utf-8
# author:xsl


from bson import ObjectId
from mongoengine import (
        StringField,
        IntField,
        BooleanField,
        ObjectIdField,
        ListField,
        DictField,
        DataTimeField,
        Document,
        )

class Source(Document):
    id = ObjectIdField(primary_key=True, default=ObjectId)
    name = StringField()
    desc = StringField()
    url = StringField()
    type = StringField()
