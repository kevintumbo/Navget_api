import datetime
from app import db
import json
from bson import json_util
from flask import current_app
from flask_bcrypt import check_password_hash, generate_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


class User(db.Document):
    """ creates an entry of the user in the database """
    first_name = db.StringField(max_length=20, min_length=1)
    last_name = db.StringField(max_length=20, min_length=1)
    username = db.StringField(max_length=30, min_length=1, unique=True)
    email = db.EmailField(max_length=120, unique=True)
    password = db.StringField(max_length=120)
    ip_address = db.StringField(max_length=24)
    last_login = db.DateTimeField(default=datetime.datetime.utcnow)
    date_created = db.DateTimeField(default=datetime.datetime.utcnow)
    date_updated = db.DateTimeField(default=datetime.datetime.utcnow,  onupdate=datetime.datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """ Initialize the user with the first name, last name, username,
            email and his password
        """
        super(User, self).__init__(*args, **kwargs)

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=600):
        """
        generate a token for authentication
        :param expiration:
        :return: token
        """
        token = Serializer(current_app.config.get('SECRET'), expires_in=expiration)
        return token.dumps(json_util.dumps({'id': self.id}))

    @staticmethod
    def verify_auth_token(token):
        """
        used to decode token and verify a user
        :param token:
        :return:
        """
        deserializer = Serializer(current_app.config.get('SECRET'))
        try:
            data = deserializer.loads(token)
            data_dict = json.loads(data)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.objects.get(id=data_dict['id']['$oid'])
        return user


class Stores(db.Document):
    """ creates a new store in the database """
    store_name = db.StringField(max_length=120, unique=True)
    store_type = db.StringField(max_length=25, nullable=False)
    store_category = db.StringField(max_length=30, nullable=False)
    location = db.ListField(db.DictField())
    date_created = db.DateTimeField(default=datetime.datetime.utcnow)
    date_updated = db.DateTimeField(default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    owner_id = db.ReferenceField(User)


class Items(db.Document):
    """ creates new item belonging to a shop """

    item_name = db.StringField(max_length=120, required=True)
    item_price = db.IntField(max_length=15, nullable=False)
    item_description = db.StringField(max_length=120, nullable=False)
    item_category = db.StringField(max_length=20, nullable=False)
    item_subcategory = db.StringField(max_length=20, nullable=False)
    item_attributes = db.DictField()
    date_created = db.DateTimeField(default=datetime.datetime.now)
    date_updated = db.DateTimeField(default=datetime.datetime.now, onupdate=datetime.datetime.now)
    item_identifier = db.StringField(max_length=25, nullable=False)
    owner_id = db.ReferenceField(User)
    store_id = db.ReferenceField(Stores)


class Services(db.Document):
    """ create new services belonging to a shop """

    service_name = db.StringField(max_length=120, required=True)
    service_price = db.IntField(max_length=15, nullable=False)
    service_description = db.StringField(max_length=120, nullable=False)
    service_category = db.StringField(max_length=20, nullable=False)
    service_subcategory = db.StringField(max_length=20, nullable=False)
    service_attributes = db.DictField()
    date_created = db.DateTimeField(default=datetime.datetime.now)
    date_updated = db.DateTimeField(default=datetime.datetime.now, onupdate=datetime.datetime.now)
    service_identifier = db.StringField(max_length=25, nullable=False)
    owner_id = db.ReferenceField(User)
    store_id = db.ReferenceField(Stores)
