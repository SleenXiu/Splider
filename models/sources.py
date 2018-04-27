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
        DateTimeField,
        Document,
        )

class Source(Document):
    meta = {
        'db_alias': 'testdb',
        'index_background': True,
        'indexes': [],
    }
    
    id = ObjectIdField(primary_key=True, default=ObjectId)
    userid = ObjectIdField()
    name = StringField()
    desc = StringField()
    url = StringField()
    type = StringField()
    thirdid = StringField()
    extra = StringField()

    def save(self, *args, **kwargs):
        return super(Source, self).save(*args, **kwargs)
