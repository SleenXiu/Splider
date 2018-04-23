# coding=utf-8
# author:xsl

from mongoengine import (
        StringField, 
        IntField, 
        BooleanField,
        ListField,
        DictField,
        ObjectIdField,
        Document,
        DateTimeField,
)
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_login import UserMixin, AnonymousUserMixin
from admin import login_manager
from bson import ObjectId

class User(UserMixin, Document):
    meta = {
        'db_alias': 'testdb',
        'index_background': True,
        'indexes': [
            'key',
        ],
    }
    
    id = ObjectIdField(primary_key=True, default=ObjectId)
    key = StringField()
    third_id = StringField()
    third_type = StringField()
    name = StringField()
    avatar = StringField()
    extra = DictField()
    create_at = DateTimeField(default=datetime.datetime.now)

    email = StringField()
    password = StringField()
    phone = StringField()
    type = IntField()

    def save(self, *args, **kwargs):
        if self.password:
            self.password = generate_password_hash(self.password)
        return super(User, self).save(*args, **kwargs)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymus(self):
        return False

    def get_id(self):
        print(self.id)
        return str(self.id)

class AnonymouseUser(AnonymousUserMixin):
    def is_authenticated(self):
        return False

login_manager.anonymous_user = AnonymouseUser

@login_manager.user_loader
def load_user(id):
    print(id)
    u = User.objects(id=ObjectId(id)).first()
    return u