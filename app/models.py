import datetime
from datetime import timedelta
from app import db
from flask import current_app
from flask_bcrypt import Bcrypt
import jwt


class User(db.Model):
    """ creates an entry of the user in the database """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    username = db.Column(db.String(30), unique=True, index=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    ip_address = db.Column(db.String(24))
    last_login = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_active = db.Column(db.Boolean(), nullable=False, default=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                             onupdate=datetime.datetime.utcnow)
    shops = db.relationship('Shops', backref='users', lazy='dynamic')
    shop_items = db.relationship('Items', backref='users', lazy='dynamic')
    shop_services = db.relationship('Services', backref='users', lazy='dynamic')

    def __init__(self, first_name, last_name, username, email, password):
        """ Intialize the user with the first name, last name, username,
            email and his password
        """
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """

        return Bcrypt().check_password_hash(self.password, password)

    def __repr__(self):
        return "{}, {}, {}".format(
            self.first_name,
            self.last_name,
            self.last_login
        )
    def generate_token(self, id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.datetime.utcnow()+ timedelta(minutes=30),
                'iat': datetime.datetime.utcnow(),
                'sub': id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

    def save(self):
        """ add new user to database"""

        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ delete user from database """

        db.session.delete(self)
        db.session.commit()

class Shops(db.Model):
    """ creates a new shop in the database """

    __tablename__ = 'shops'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shop_name = db.Column(db.String(120), unique=True)
    shop_type = db.Column(db.String(15), nullable=False)
    shop_category = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=True)
    county = db.Column(db.String(30), nullable=True)
    town_city = db.Column(db.String(30), nullable=True)
    physical_address = db.Column(db.String(100), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                             onupdate=datetime.datetime.utcnow)
    items = db.relationship('Items', backref='shops', lazy='dynamic', cascade='delete')
    services = db.relationship('Services', backref='shops', lazy='dynamic', cascade='delete')
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "{}, {}, {}, {}, {}".format(
            self.shop_name,
            self.shop_type,
            self.shop_category,
            self.date_created,
            self.date_modifed
        )
 
    @staticmethod
    def get_all_shops():
        """ reutrn all shops in a single query """
        return Shops.query.all()

    def save(self):
        """ save shop in db """

        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ delete shop in db """
        db.session.delete(self)
        db.session.commit()


class Items(db.Model):
    """ creates new item belonging to a shop """

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(120), unique=True)
    item_price = db.Column(db.String(15), nullable=False)
    item_description = db.Column(db.String(120), nullable=False)
    item_category = db.Column(db.String(20), nullable=False)
    item_subcategory = db.Column(db.String(20), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))

    def __repr__(self):
        return "{}, {}, {}, {}, {}".format(
            self.item_name,
            self.item_price,
            self.item_description,
            self.date_created,
            self.date_modifed
        )

    @staticmethod
    def get_all_items():
        """ get all items in db """

        return Items.query.all()

    def save(self):
        """ save item in db """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ delete item from db """
        db.session.delete(self)
        db.session.commit()


class Services(db.Model):
    """ create new services belonging to a shop """

    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_name = db.Column(db.String(120), unique=True)
    service_price = db.Column(db.String(15), nullable=False)
    service_description = db.Column(db.String(120), nullable=False)
    service_category = db.Column(db.String(20), nullable=False)
    service_subcategory = db.Column(db.String(20), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))

    def __repr__(self):
        return "{}, {}, {}, {}, {}".format(
            self.service_name,
            self.service_price,
            self.service_description,
            self.date_created,
            self.date_modifed
        )

    @staticmethod
    def get_all_services():
        """ get all items in a single query """
        return Services.query.all()

    def save(self):
        """ save service in db """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ delete service in db """
        db.session.delete(self)
        db.session.commit()
