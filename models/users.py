# coding=utf-8
# author:xsl

from mongoengine import (
        StringField, 
        IntField, 
        BooleanField,
        ListField,
        DictField,
        ObjectIdField,
        Document
)
from bson import ObjectId

class User(Document):
    
    id = ObjectIdField(primary_key=True, default=ObjectId)
    third_id = StringField()
    third_type = StringField()
    name = StringField()
    avatar = StringField()
    extra = DictField()


