from flask import g, jsonify
import json
import datetime
from bson import json_util
import re
import string
import random
from flask_restful import Resource, Api, reqparse
from flask_httpauth import HTTPTokenAuth
from . import store_blueprint
from ..models import User, Stores, Items, Services

api_store = Api(store_blueprint)
auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    """
    :param token:
    :return: Boolean
    """
    # try to authenticate by token
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


def my_converter(o):
    """
    serialize datetime
    :param o:
    :return:
    """
    if isinstance(o, datetime.datetime):
        return o.__str__()


def id_generator(size=25, chars=string.ascii_lowercase + string.digits):
    """
    generate item or service id
    :param size:
    :param chars:
    :return:
    """
    identifier = ''.join(random.choice(chars) for _ in range(size))
    return identifier


class Store(Resource):
    """
    Api resource for handling the store
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('store_name', required=True, help="Error. Missing Store Name.")
        self.parser.add_argument('store_type', required=True, help="Error. Missing Store Type.")
        self.parser.add_argument('store_category', required=True, help="Error. Missing Store Category.")
        self.parser.add_argument('location', required=True, type=dict, help="Error. Missing Location Field.",
                                 action='append')
        self.parser.add_argument('page_no', default=1)
        self.parser.add_argument('limit', default=20,)
        self.parser.add_argument('q', default="")

    @auth.login_required
    def post(self):
        """
        POST request to create a store
        :return:
        """

        args = self.parser.parse_args()

        # confirm store name value exists and is of valid format
        store_name = args['store_name']
        if not store_name:
            response = {
                'message': 'Error. Missing Store Name.'
            }
            # return a response notifying them that store name is missing
            return response, 400

        check_store_name = re.match('^[a-z A-Z0-9_.-]+$', store_name)
        if check_store_name is None:
            response = {
                'message': 'Error. Store Name Has Invalid Characters.'
            }
            # return a response notifying the user that credentials store name is invalid
            return response, 400

        # Confirm store type exists
        store_type = args['store_type']
        if not store_type:
            response = {
                'message': 'Error. Missing Store Type.'
            }
            # return a response notifying them that store Type is missing
            return response, 400

        # confirm store category exists
        store_category = args['store_category']
        if not store_category:
            response = {
                'message': 'Error. Missing Store category.'
            }
            # return a response notifying them that Store Category is missing
            return response, 400

        if store_category != 'online store':
            location = args['location']

            if not location:
                response = {
                    'message': 'Error. Missing Store Location.'
                }
                # return a response notifying them that Store Location is missing
                return response, 400
            for loc in location:
                for key, value in loc.items():
                    if key == "country":
                        # confirm country field exists
                        country = value
                        if not country:
                            response = {
                                'message': 'Error. Missing Country field.'
                            }
                            # return a response notifying them that Country is missing
                            return response, 400
                    if key == "county":
                        # confirm county field exists
                        county = value
                        if not county:
                            response = {
                                'message': 'Error. Missing County field.'
                            }
                            # return a response notifying them that county is missing
                            return response, 400

                    if key == "town_city":
                        # confirm town/city field exists
                        town_city = value
                        if not town_city:
                            response = {
                                'message': 'Error. Missing City/Town field.'
                            }

                            # return a response notifying them that City/Town field is missing
                            return response, 400
                    if key == "area":
                        # confirm area exists
                        area = value
                        if not area:
                            response = {
                                'message': "Error. Missing area field"
                            }

                    if key == "physical_address":
                        # confirm  physical address exists
                        physical_address = value
                        if not physical_address:
                            response = {
                                'message': 'Error. Missing physical address field.'
                            }

                            # return a response notifying them that City/Town field is missing
                            return response, 400

                        # check if physical address has invalid characters
                        check_physical_address = re.match('^[a-z A-Z0-9_.,-]+$', physical_address)
                        if check_physical_address is None:
                            response = {
                                'message': 'Error. Physical Address Has Invalid Characters.'
                            }
                            # return a response notifying the user that credentials shop name is invalid
                            return response, 400

        if store_category == 'online store':
            location = 'online store'
        # Query to see if shop name already exists
        try:
            store_name = Stores.objects.get(store_name=store_name, owner_id=g.user.id)
        except Stores.DoesNotExist:
            store_name = None

        if not store_name:
            # if shop name does not exist, we can create the shop.
            try:
                store = Stores(
                    store_name=args['store_name'],
                    store_type=args['store_type'],
                    store_category=args['store_category'],
                    location=location,
                    owner_id=g.user.id)
                store.save()

                response = jsonify({
                    "store_id": json.dumps(store.id, default=json_util.default),
                    "store_name": store.store_name,
                    "store_type": store.store_type,
                    "store_category": store.store_category,
                    "location": store.location,
                    'message': 'Success. You have created your store.'
                })
                response.status_code = 201
                return response
            except Exception as e:
                # An error has occurred, therefore return a string message containing the error
                response = {
                    'status': 'error',
                    'message': str(e)
                }
                return response, 500
        response = {
            'message': 'Sorry that shop name already exists. Please Pick another one.'
        }

        return response, 409

    @auth.login_required
    def get(self, id=None):
        """
        GET request to retrieve list of all stores owned by the user
        """
        # GET request
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('id', location='args')
        get_parser.add_argument('page_no', default=1, location='args')
        get_parser.add_argument('limit', default=20, location='args')
        get_parser.add_argument('q', default="", location='args', type=str)
        args = get_parser.parse_args()
        page_no = args['page_no']
        limit = args['limit']
        q = args['q']

        if id:
            try:
                single_store = Stores.objects.get(owner_id=g.user.id, id=id)
            except Stores.DoesNotExist:
                single_store = None
            if not single_store:
                response = {
                    'message': 'Stores not found.'
                }
                return response, 404
            response = jsonify({
                "store_name": single_store.store_name,
                "store_type": single_store.store_type,
                "store_category": single_store.store_category,
                "location": single_store.location
            })
            response.status_code = 200
            return response

        # Query to see if store name already exists
        try:
            all_stores = Stores.objects(owner_id=g.user.id)
        except Stores.DoesNotExist:
            all_stores = None

        if not all_stores:
            response = {
                'message': 'You have not created any store.'
            }
            return response, 404
        response = jsonify({
            'Stores': [
                {
                    "store_id": json.dumps(store.id, default=json_util.default),
                    "store_name": store.store_name,
                    "store_type": store.store_type,
                    "store_category": store.store_category,
                    "location": store.location,
                    "date_created": store.date_created,
                    "date_updated": store.date_updated
                } for store in all_stores
            ],
        })
        response.status_code = 200
        return response

    @auth.login_required
    def put(self, id=None):
        """
        PUT request to edit details of a store
        :return: response
        """
        if not id:
            response = {
                'message': 'Store not found.'
            }
            return response, 404

        # query the database for the Store with the id
        try:
            store = Stores.objects.get(owner_id=g.user.id, id=id)
        except Stores.DoesNotExist:
            store = None

        if not store:
            response = {
                'message': 'That Store does not exist.'
            }
            return response, 404

        args = self.parser.parse_args()

        # confirm store name value exists and is of valid format
        store_name = args['store_name']
        if not store_name:
            response = {
                'message': 'Error. Missing Store Name.'
            }
            # return a response notifying them that Store name is  missing
            return response, 400

        check_store_name = re.match('^[a-z A-Z0-9_.-]+$', store_name)
        if check_store_name is None:
            response = {
                'message': 'Error. Store Name Has Invalid Characters.'
            }
            # return a response notifying the user that credentials Store name is invalid
            return response, 400

        # Confirm store type exists
        store_type = args['store_type']
        if not store_type:
            response = {
                'message': 'Error. Missing Store Type.'
            }
            # return a response notifying them that Store Type is missing
            return response, 400

        # confirm store category exists
        store_category = args['store_category']
        if not store_category:
            response = {
                'message': 'Error. Missing Store category.'
            }
            # return a response notifying them that Store Category is missing
            return response, 400

        if store_category != 'online store':
            location = args['location']
            if not location:
                response = {
                    'message': 'Error. Missing Store Location.'
                }
                # return a response notifying them that Store Location is missing
                return response, 400
            for loc in location:
                for key, value in loc.items():
                    if key == "country":
                        # confirm country field exists
                        country = value
                        if not country:
                            response = {
                                'message': 'Error. Missing Country field.'
                            }
                            # return a response notifying them that Country is missing
                            return response, 400
                    if key == "county":
                        # confirm county field exists
                        county = value
                        if not county:
                            response = {
                                'message': 'Error. Missing County field.'
                            }
                            # return a response notifying them that county is missing
                            return response, 400

                    if key == "town_city":
                        # confirm town/city field exists
                        town_city = value
                        if not town_city:
                            response = {
                                'message': 'Error. Missing City/Town field.'
                            }

                            # return a response notifying them that City/Town field is missing
                            return response, 400
                    if key == "area":
                        # confirm area exists
                        area = value
                        if not area:
                            response = {
                                'message': "Error. Missing area field"
                            }

                    if key == "physical_address":
                        # confirm  physical address exists
                        physical_address = value
                        if not physical_address:
                            response = {
                                'message': 'Error. Missing physical address field.'
                            }

                            # return a response notifying them that City/Town field is missing
                            return response, 400

                        # check if physical address has invalid characters
                        check_physical_address = re.match('^[a-z A-Z0-9_.,-]+$', physical_address)
                        if check_physical_address is None:
                            response = {
                                'message': 'Error. Physical Address Has Invalid Characters.'
                            }
                            # return a response notifying the user that credentials shop name is invalid
                            return response, 400

        if store_category == 'online store':
            location = 'online store'

        store.store_name = store_name
        store.store_type = store_type
        store.store_category = store_category
        store.location = location
        store.save()

        response = {
            "store_id": json.dumps(store.id, default=json_util.default),
            "store_name": store.store_name,
            "store_type": store.store_type,
            "store_category": store.store_category,
            "location": store.location,
            "message": "Success. You have edited {}'s information.".format(store.store_name)
        }

        return response, 200

    @auth.login_required
    def delete(self, id=None):
        """
        Delete Request to delete Store details
        :return:
        """
        if not id:
            response = {
                "message": "Please Select an existing store"
            }
            return response, 404

        # query to see if Store exists
        try:
            store = Stores.objects.get(owner_id=g.user.id, id=id)
        except Stores.DoesNotExist:
            store = None

        if not store:
            response = {
                "message": "That Store does not exist."
            }
            return response, 404
        store_name = store.store_name
        store.delete()
        response = {
            "message": "You have successfully deleted the shop {}".format(store_name)
        }
        return response, 200


class Item(Resource):
    """
    Api Resource for store items
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('item_name', required=True, help="Error. Missing Item Name.")
        self.parser.add_argument('item_price', required=True, help="Error. Missing Item Price.")
        self.parser.add_argument('item_description', required=True, help="Error. Missing Item Description.")
        self.parser.add_argument('item_category', required=True, help="Error. Missing Item Category.")
        self.parser.add_argument('item_subcategory', required=True, help="Error. Missing Item Subcategory.")
        self.parser.add_argument('item_attributes',  type=dict)
        self.parser.add_argument('store_id', location='args')
        self.parser.add_argument('item_id', location='args')
        self.parser.add_argument('page_no', default=1)
        self.parser.add_argument('limit', default=20, )
        self.parser.add_argument('q', default="")

    @auth.login_required
    def post(self, store_id=None):
        """
        POST REQUEST
        Add an item to a store
        :return:
        """
        args = self.parser.parse_args()
        if not store_id:
            response = {
                "message": "Please Select an existing store."
            }
            return response, 404

        try:
            store = Stores.objects.get(owner_id=g.user.id, id=store_id)
        except Stores.DoesNotExist:
            store = None

        if not store:
            response = {
                "message": "That shop does not exist."
            }
            return response, 404

        # confirm item name exists and is of valid format
        item_name = args['item_name']
        if not item_name:
            response = {
                'message': 'Error. Missing Item Name.'
            }
            # return a response notifying them that item name is missing
            return response, 400

        check_item_name = re.match('^[a-z A-Z0-9_.()-]+$', item_name)
        if check_item_name is None:
            response = {
                'message': 'Error. Item Name Has Invalid Characters.'
            }
            # return a response notifying the user that credentials item name is invalid
            return response, 400

        # confirm item_description exists and is of valid format
        item_description = args['item_description']
        if not item_description:
            response = {
                'message': 'Error. Missing Item Description.'
            }
            # return a response notifying them that item description is missing
            return response, 400

        check_item_description = re.match('^[a-z A-Z0-9_.()-]+$', item_description)
        if check_item_description is None:
            response = {
                'message': 'Error. Item Description Has Invalid Characters.'
            }
            # return a response notifying the user that credentials item description is invalid
            return response, 400

        # confirm item_price exists and is of valid format
        item_price = args['item_price']
        if not item_price:
            response = {
                'message': 'Error. Missing Item price.'
            }
            # return a response notifying them that item price is  missing
            return response, 400

        check_item_price = re.match('^[ 0-9-]+$', item_price)
        if check_item_price is None:
            response = {
                'message': 'Error. Item price Has Invalid Characters.'
            }
            # return a response notifying the user that credentials item price is invalid
            return response, 400

        # confirm item_category exists
        item_category = args['item_category']
        if not item_category:
            response = {
                'message': 'Error. Missing Item Category.'
            }
            # return a response notifying them that item category is  missing
            return response, 400

        # confirm item_subcategory exists
        item_subcategory = args['item_subcategory']
        if not item_subcategory:
            response = {
                'message': 'Error. Missing Item Subcategory.'
            }
            # return a response notifying them that item subcategory is missing
            return response, 400

        # check if item attributes have invalid characters
        item_attributes = args['item_attributes']
        if item_attributes:
            for name, value in item_attributes.items():
                if not name:
                    response = {
                        "message": 'attribute name cannot be empty.'
                    }
                    return response, 400
                check_attribute_name = re.match('^[a-z A-Z0-9_.,-]+$', name)
                if not check_attribute_name:
                    response = {
                        "message": '{} is not a valid attribute name'.format(name)
                    }
                    return response, 400
                if not value:
                    response = {
                        "message": 'attribute value cannot be Empty.'
                    }
                    return response, 400
                check_attribute_value = re.match('^[a-z A-Z0-9_.,-]+$', value)
                if not check_attribute_value:
                    response = {
                        "message": '{} is not a valid attribute value'.format(value)
                    }
                    return response, 400

        # Query to see if item name already exists in current store
        try:
            item_name = Items.objects.get(item_name=item_name, owner_id=g.user.id, store_id=store_id)
        except Items.DoesNotExist:
            item_name = None

        identifier = id_generator()

        if not item_name:
            # if item name does not exist, we can create the item.
            try:
                item = Items(
                            item_name=args['item_name'],
                            item_price=args['item_price'],
                            item_description=args['item_description'],
                            item_category=args['item_category'],
                            item_subcategory=args['item_subcategory'],
                            item_attributes=args['item_attributes'],
                            item_identifier=identifier,
                            store_id=store_id,
                            owner_id=g.user.id)
                item.save()

                response = jsonify({
                    "item_identifier": item.item_identifier,
                    "item_name": item.item_name,
                    "item_price": item.item_price,
                    "item_description": item.item_description,
                    "item_category": item.item_category,
                    "item_subcategory": item.item_subcategory,
                    "item_attributes": item.item_attributes,
                    'message': 'Success. You have added {} to the store.'.format(item.item_name)
                })
                response.status_code = 201
                return response
            except Exception as e:
                # An error has occurred, therefore return a string message containing the error
                response = {
                    'status': 'error',
                    'message': str(e)
                }
                return response, 500
        response = {
            'message': 'Sorry. {} already exists in this store. Please rename the Item'.format(args['item_name'])
        }

        return response, 409

    @auth.login_required
    def get(self, store_id=None, item_id=None):
        """
        GET REQUEST
        Get an item from a store

        :return:
        """
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('store_id', location='args')
        get_parser.add_argument('item_id', location='args')
        get_parser.add_argument('page_no', default=1, location='args')
        get_parser.add_argument('limit', default=20, location='args')
        get_parser.add_argument('q', default="", location='args', type=str)

        args = get_parser.parse_args()
        page_no = args['page_no']
        limit = args['limit']
        q = args['q']

        if not store_id:
            response = {
                "message": "Please Select an existing Store."
            }
            return response, 404

        try:
            store = Stores.objects.get(owner_id=g.user.id, id=store_id)
        except Stores.DoesNotExist:
            store = None
        # check if store exists
        if not store:
            response = {
                "message": "That Store does not exist."
            }
            return response, 404

        # get all items in a store
        if not item_id:
            try:
                items = Items.objects(owner_id=g.user.id, store_id=store_id)
            except Items.DoesNotExist:
                items = None

            if not items:
                response = {
                    'message': 'You have not added any items to the store.'
                }
                return response, 404

            response = jsonify({
                'items': [
                    {
                        "item_id": json.dumps(item.id, default=json_util.default),
                        "item_identifier": item.item_identifier,
                        "item_name": item.item_name,
                        "item_price": item.item_price,
                        "item_description": item.item_description,
                        "item_category": item.item_category,
                        "item_subcategory": item.item_subcategory,
                        "item_attributes": item.item_attributes,
                        "date_created": item.date_created,
                        "date_updated": item.date_updated
                    } for item in items
                ],
            })
            response.status_code = 200
            return response

        # Get specific item from a shop
        try:
            item = Items.objects.get(owner_id=g.user.id, store_id=store_id, item_identifier=item_id)
            print (item)
        except Items.DoesNotExist:
            item = None

        if not item:
            response = {
                "message": "Item does not exist."
            }
            return response, 404

        response = {
            "item_id": json.dumps(item.id, default=json_util.default),
            "item_identifier": item.item_identifier,
            "item_name": item.item_name,
            "item_price": item.item_price,
            "item_description": item.item_description,
            "item_category": item.item_category,
            "item_subcategory": item.item_subcategory,
            "item_attributes": item.item_attributes,
            "date_created": json.dumps(item.date_created, default=my_converter),
            "date_updated": json.dumps(item.date_updated, default=my_converter)
        }
        return response, 200

    @auth.login_required
    def put(self, store_id=None, item_id=None):
        """
        PUT REQUEST
        update an item in a store
        :return:
        """
        # check if store id exists
        if not store_id:
            response = {
                "message": "Please Select an existing store."
            }
            return response, 404
        try:
            store = Stores.objects.get(owner_id=g.user.id, id=store_id)
        except Stores.DoesNotExist:
            store = None

        # check if store exists
        if not store:
            response = {
                "message": "That store does not exist."
            }
            return response, 404

        # get item from store
        if not item_id:
            response = {
                "message": "Please Select an item."
            }
            return response, 404

        try:
            item = Items.objects.get(owner_id=g.user.id, store_id=store_id, item_identifier=item_id)
        except Items.DoesNotExist:
            item = None

        if not item:
            response = {
                "message": "Item does not exist."
            }
            return response, 404

        args = self.parser.parse_args()
        # confirm item name exists and is of valid format
        item_name = args['item_name']
        if not item_name:
            response = {
                'message': 'Error. Missing Item Name.'
            }
            # return a response notifying them that item name is missing
            return response, 400

        check_item_name = re.match('^[a-z A-Z0-9_.()-]+$', item_name)
        if check_item_name is None:
            response = {
                'message': 'Error. Item Name Has Invalid Characters.'
            }
            # return a response notifying the user that credentials item name is invalid
            return response, 400

        # confirm item_description exists and is of valid format
        item_description = args['item_description']
        if not item_description:
            response = {
                'message': 'Error. Missing Item Description.'
            }
            # return a response notifying them that item description is missing
            return response, 400

        check_item_description = re.match('^[a-z A-Z0-9_.()-]+$', item_description)
        if check_item_description is None:
            response = {
                'message': 'Error. Item Description Has Invalid Characters.'
            }
            # return a response notifying the user that credentials item description is invalid
            return response, 400

        # confirm item_price exists and is of valid format
        item_price = args['item_price']
        if not item_price:
            response = {
                'message': 'Error. Missing Item price.'
            }
            # return a response notifying them that item price is  missing
            return response, 400

        check_item_price = re.match('^[ 0-9-]+$', item_price)
        if check_item_price is None:
            response = {
                'message': 'Error. Item price Has Invalid Characters.'
            }
            # return a response notifying the user that credentials item price is invalid
            return response, 400

        # confirm item_category exists
        item_category = args['item_category']
        if not item_category:
            response = {
                'message': 'Error. Missing Item Category.'
            }
            # return a response notifying them that item category is  missing
            return response, 400

        # confirm item_subcategory exists
        item_subcategory = args['item_subcategory']
        if not item_subcategory:
            response = {
                'message': 'Error. Missing Item Subcategory.'
            }
            # return a response notifying them that item subcategory is missing
            return response, 400

        # check if item attributes have invalid characters
        item_attributes = args['item_attributes']
        if item_attributes:
            for name, value in item_attributes.items():
                if not name:
                    response = {
                        "message": 'attribute name cannot be Empty.'
                    }
                    return response, 400
                check_attribute_name = re.match('^[a-z A-Z0-9_.,-]+$', name)
                if not check_attribute_name:
                    response = {
                        "message": '{} is not a valid attribute name'.format(name)
                    }
                    return response, 400
                if not value:
                    response = {
                        "message": 'attribute value cannot be Empty.'
                    }
                    return response, 400
                check_attribute_value = re.match('^[a-z A-Z0-9_.,-]+$', value)
                if not check_attribute_value:
                    response = {
                        "message": '{} is not a valid attribute value'.format(value)
                    }
                    return response, 400

        item.item_name = item_name
        item.item_price = item_price
        item.item_description = item_description
        item.item_category = item_category
        item.item_subcategory = item_subcategory
        item.item_attributes = item_attributes
        item.save()

        response = {
            "item_id": json.dumps(item.id, default=json_util.default),
            "item_name": item.item_name,
            "item_price": item.item_price,
            "item_description": item.item_description,
            "item_category": item.item_category,
            "item_subcategory": item.item_subcategory,
            "item_attributes": item.item_attributes,
            "item_identifier": item.item_identifier,
            "date_created": json.dumps(item.date_created, default=my_converter),
            "date_updated": json.dumps(item.date_updated, default=my_converter),
            "message": "You have successfully updated {}".format(item.item_name)
        }
        return response, 200

    @auth.login_required
    def delete(self, store_id=None, item_id=None):
        """
        DELETE Request
        delete an item from the store
        :return:
        """

        if not store_id:
            response = {
                "message": "Please Select an existing shop."
            }
            return response, 404
        try:
            store = Stores.objects.get(owner_id=g.user.id, id=store_id)
        except Stores.DoesNotExist:
            store = None
        # check if store exists
        if not store:
            response = {
                "message": "That Store does not exist."
            }
            return response, 404

        # get item from store
        if not item_id:
            response = {
                "message": "Please Select an item."
            }
            return response, 404
        try:
            item = Items.objects.get(owner_id=g.user.id, store_id=store_id, item_identifier=item_id)
        except Items.DoesNotExist:
            item = None
        if not item:
            response = {
                "message": "Item does not exist."
            }
            return response, 404
        store_name = store.store_name
        item_name = item.item_name

        item.delete()
        response = {
            "message": "You have successfully deleted {} from the store {}".format(item_name, store_name)
        }
        return response, 200


class Service(Resource):
    """
    Api Resource for store services
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('service_name', required=True, help="Error. Missing Item Name.")
        self.parser.add_argument('service_price', required=True, help="Error. Missing Item Price.")
        self.parser.add_argument('service_description', required=True, help="Error. Missing Item Description.")
        self.parser.add_argument('service_category', required=True, help="Error. Missing Item Category.")
        self.parser.add_argument('service_subcategory', required=True, help="Error. Missing Item Subcategory.")
        self.parser.add_argument('service_attributes', type=dict)
        self.parser.add_argument('store_id', location='args')
        self.parser.add_argument('item_id', location='args')
        self.parser.add_argument('page_no', default=1)
        self.parser.add_argument('limit', default=20, )
        self.parser.add_argument('q', default="")

    @auth.login_required
    def post(self, store_id=None):
        """

        :param store_id:
        :return: Json response of service created
        """
        args = self.parser.parse_args()
        if not store_id:
            response = {
                "message": "Please Select an existing shop."
            }
            return response, 404
        try:
            store = Stores.objects.get(owner_id=g.user.id, id=store_id)
        except Stores.DoesNotExist:
            store = None

        if not store:
            response = {
                "message": "That Store does not exist."
            }
            return response, 404

        # confirm Service name exists and is of valid format
        service_name = args['service_name']
        if not service_name:
            response = {
                'message': 'Error. Missing Service Name.'
            }
            # return a response notifying them that Service name is missing
            return response, 400

        check_service_name = re.match('^[a-z A-Z0-9_.()-]+$', service_name)
        if check_service_name is None:
            response = {
                'message': 'Error. Service Name Has Invalid Characters.'
            }
            # return a response notifying the user that credentials Service name is invalid
            return response, 400

        # confirm service_description exists and is of valid format
        service_description = args['service_description']
        if not service_description:
            response = {
                'message': 'Error. Missing Service Description.'
            }
            # return a response notifying them that service description is missing
            return response, 400

        check_service_description = re.match('^[a-z A-Z0-9_.?()-]+$', service_description)
        if check_service_description is None:
            response = {
                'message': 'Error. Service Description Has Invalid Characters.'
            }
            # return a response notifying the user that credentials Service description is invalid
            return response, 400

        # confirm service_price exists and is of valid format
        service_price = args['service_price']
        if not service_price:
            response = {
                'message': 'Error. Missing Service price.'
            }
            # return a response notifying them that Service price is  missing
            return response, 400

        check_service_price = re.match('^[ 0-9-]+$', service_price)
        if check_service_price is None:
            response = {
                'message': 'Error. Service price Has Invalid Characters.'
            }
            # return a response notifying the user that credentials Service price is invalid
            return response, 400

        # confirm service_category exists
        service_category = args['service_category']
        if not service_category:
            response = {
                'message': 'Error. Missing Service Category.'
            }
            # return a response notifying them that Service category is missing
            return response, 400

        # confirm service_subcategory exists
        service_subcategory = args['service_subcategory']
        if not service_subcategory:
            response = {
                'message': 'Error. Missing Service Subcategory.'
            }
            # return a response notifying them that Service subcategory is missing
            return response, 400
        # check if service attributes have invalid characters
        service_attributes = args['service_attributes']
        if service_attributes:
            for name, value in service_attributes.items():
                if not name:
                    response = {
                        "message": 'attribute name cannot be empty.'
                    }
                    return response, 400
                check_attribute_name = re.match('^[a-z A-Z0-9_.,-]+$', name)
                if not check_attribute_name:
                    response = {
                        "message": '{} is not a valid attribute name'.format(name)
                    }
                    return response, 400
                if not value:
                    response = {
                        "message": 'attribute value cannot be Empty.'
                    }
                    return response, 400
                check_attribute_value = re.match('^[a-z A-Z0-9_.,-]+$', value)
                if not check_attribute_value:
                    response = {
                        "message": '{} is not a valid attribute value'.format(value)
                    }
                    return response, 400
        # Query to see if Service name already exists in current store
        try:
            service_name = Services.objects.get(service_name=service_name, owner_id=g.user.id, store_id=store_id)
        except Services.DoesNotExist:
            service_name = None

        if not service_name:
            # if shop name does not exist, we can create the shop.
            identifier = id_generator()
            try:
                service = Services(
                    service_name=args['service_name'],
                    service_price=args['service_price'],
                    service_description=args['service_description'],
                    service_category=args['service_category'],
                    service_subcategory=args['service_subcategory'],
                    service_attributes=args['service_attributes'],
                    service_identifier=identifier,
                    store_id=store_id,
                    owner_id=g.user.id)
                service.save()

                response = jsonify({
                    "service_id": json.dumps(service.id, default=json_util.default),
                    "service_name": service.service_name,
                    "service_price": service.service_price,
                    "service_description": service.service_description,
                    "service_category": service.service_category,
                    "service_subcategory": service.service_subcategory,
                    "service_attributes": service.service_attributes,
                    "service_identifier": service.service_identifier,
                    "date_created": service.date_created,
                    "date_updated": service.date_updated,
                    'message': 'Success. You have added a new Service {} to the store.'.format(args['service_name'])
                })
                response.status_code = 201
                return response
            except Exception as e:
                # An error has occurred, therefore return a string message containing the error
                response = {
                    'status': 'error',
                    'message': str(e)
                }
                return response, 500
        response = {
            'message': 'Sorry. {} already exists in this store.'.format(args['service_name'])
        }

        return response, 409

    @auth.login_required
    def get(self, store_id=None, service_id=None):
        """
        GET REQUEST
        Get an service from a store

        :return:
        """
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('store_id', location='args')
        get_parser.add_argument('item_id', location='args')
        get_parser.add_argument('page_no', default=1, location='args')
        get_parser.add_argument('limit', default=20, location='args')
        get_parser.add_argument('q', default="", location='args', type=str)

        args = get_parser.parse_args()
        page_no = args['page_no']
        limit = args['limit']
        q = args['q']

        if not store_id:
            response = {
                "message": "Please Select an existing Store."
            }
            return response, 404
        try:
            store = Stores.objects.get(owner_id=g.user.id, id=store_id)
        except Stores.DoesNotExist:
            store = None
        # check if store exists
        if not store:
            response = {
                "message": "That Store does not exist."
            }
            return response, 404

        # get all services in a store
        if not service_id:
            try:
                services = Services.objects(owner_id=g.user.id, store_id=store_id)
            except Services.DoesNotExist:
                services = None

            if not services:
                response = {
                    'message': 'You have not added any services to the store.'
                }
                return response, 404

            response = jsonify({
                'services': [
                    {
                        "service_id": json.dumps(service.id, default=json_util.default),
                        "service_name": service.service_name,
                        "service_price": service.service_price,
                        "service_description": service.service_description,
                        "service_category": service.service_category,
                        "service_subcategory": service.service_subcategory,
                        "service_attributes": service.service_attributes,
                        "service_identifier": service.service_identifier,
                        "date_created": service.date_created,
                        "date_updated": service.date_updated
                    } for service in services
                ],
            })
            response.status_code = 200
            return response

        # Get specific service from a Store
        try:
            service = Services.objects.get(owner_id=g.user.id, store_id=store_id, service_identifier=service_id)
        except Services.DoesNotExist:
            service = None

        if not service:
            response = {
                "message": "Service does not exist."
            }
            return response, 404

        response = {
            "service_id": json.dumps(service.id, default=json_util.default),
            "service_name": service.service_name,
            "service_price": service.service_price,
            "service_description": service.service_description,
            "service_category": service.service_category,
            "service_subcategory": service.service_subcategory,
            "service_attributes": service.service_attributes,
            "service_identifier": service.service_identifier,
            "date_created": json.dumps(service.date_created, default=my_converter),
            "date_updated": json.dumps(service.date_updated, default=my_converter)
        }
        return response, 200

    @auth.login_required
    def put(self, store_id=None, service_id=None):
        """
        PUT REQUEST
        update an service in a store
        :return:
        """
        # check if store id exists
        if not store_id:
            response = {
                "message": "Please Select an existing store."
            }
            return response, 404

        # check if store exists
        try:
            store = Stores.objects.get(owner_id=g.user.id, id=store_id)
        except Stores.DoesNotExist:
            store = None

        if not store:
            response = {
                "message": "That store does not exist."
            }
            return response, 404

        # get item from store
        if not service_id:
            response = {
                "message": "Please Select an service."
            }
            return response, 404

        # Get specific service from a Store
        try:
            service = Services.objects.get(owner_id=g.user.id, store_id=store_id, service_identifier=service_id)
        except Services.DoesNotExist:
            service = None

        if not service:
            response = {
                "message": "Service does not exist."
            }
            return response, 404

        args = self.parser.parse_args()
        # confirm Service name exists and is of valid format
        service_name = args['service_name']
        if not service_name:
            response = {
                'message': 'Error. Missing Service Name.'
            }
            # return a response notifying them that Service name is missing
            return response, 400

        check_service_name = re.match('^[a-z A-Z0-9_.()-]+$', service_name)
        if check_service_name is None:
            response = {
                'message': 'Error. Service Name Has Invalid Characters.'
            }
            # return a response notifying the user that credentials Service name is invalid
            return response, 400

        # confirm service_description exists and is of valid format
        service_description = args['service_description']
        if not service_description:
            response = {
                'message': 'Error. Missing Service Description.'
            }
            # return a response notifying them that service description is missing
            return response, 400

        check_service_description = re.match('^[a-z A-Z0-9_.()-]+$', service_description)
        if check_service_description is None:
            response = {
                'message': 'Error. Service description Has Invalid Characters.'
            }
            # return a response notifying the user that credentials Service description is invalid
            return response, 400

        # confirm service_price exists and is of valid format
        service_price = args['service_price']
        if not service_price:
            response = {
                'message': 'Error. Missing Service price.'
            }
            # return a response notifying them that service price is  missing
            return response, 400

        check_service_price = re.match('^[ 0-9-]+$', service_price)
        if check_service_price is None:
            response = {
                'message': 'Error. Service price Has Invalid Characters.'
            }
            # return a response notifying the user that credentials service price is invalid
            return response, 400

        # confirm service_category exists
        service_category = args['service_category']
        if not service_category:
            response = {
                'message': 'Error. Missing Service Category.'
            }
            # return a response notifying them that service category is  missing
            return response, 400

        # confirm service_subcategory exists
        service_subcategory = args['service_subcategory']
        if not service_subcategory:
            response = {
                'message': 'Error. Missing Service Subcategory.'
            }
            # return a response notifying them that service subcategory is missing
            return response, 400

        # check if service attributes have invalid characters
        service_attributes = args['service_attributes']
        if service_attributes:
            for name, value in service_attributes.items():
                if not name:
                    response = {
                        "message": 'attribute name cannot be empty.'
                    }
                    return response, 400
                check_attribute_name = re.match('^[a-z A-Z0-9_.,-]+$', name)
                if not check_attribute_name:
                    response = {
                        "message": '{} is not a valid attribute name'.format(name)
                    }
                    return response, 400
                if not value:
                    response = {
                        "message": 'attribute value cannot be Empty.'
                    }
                    return response, 400
                check_attribute_value = re.match('^[a-z A-Z0-9_.,-]+$', value)
                if not check_attribute_value:
                    response = {
                        "message": '{} is not a valid attribute value'.format(value)
                    }
                    return response, 400

            service.service_name = service_name
            service.service_price = service_price
            service.service_description = service_description
            service.service_category = service_category
            service.service_subcategory = service_subcategory
            service.service_attributes = service_attributes
            service.save()

            response = {
                "service_id": json.dumps(service.id, default=json_util.default),
                "service_name": service.service_name,
                "service_price": service.service_price,
                "service_description": service.service_description,
                "service_category": service.service_category,
                "service_subcategory": service.service_subcategory,
                "service_attributes": service.service_attributes,
                "date_created": json.dumps(service.date_created, default=my_converter),
                "date_updated": json.dumps(service.date_updated, default=my_converter)
            }
            return response, 200

    @auth.login_required
    def delete(self, store_id=None, service_id=None):
        """
        DELETE Request
        delete an item from the store
        :return:
        """

        if not store_id:
            response = {
                "message": "Please Select an existing Store."
            }
            return response, 404
        try:
            store = Stores.objects.get(owner_id=g.user.id, id=store_id)
        except Stores.DoesNotExist:
            store = None
        # check if store exists
        if not store:
            response = {
                "message": "That Store does not exist."
            }
            return response, 404

        # get item from store
        if not service_id:
            response = {
                "message": "Please Select an Service."
            }
            return response, 404
        # Get specific service from a store
        try:
            service = Services.objects.get(owner_id=g.user.id, store_id=store_id, service_identifier=service_id)
        except Services.DoesNotExist:
            service = None
        if not service:
            response = {
                "message": "Service does not exist."
            }
            return response, 404
        store_name = store.store_name
        service_name = service.service_name

        service.delete()
        response = {
            "message": "You have successfully deleted {} the store {}".format(service_name, store_name)
        }
        return response, 200

# make resource accessible to the system
# http://127.0.0.1:5000/navyget-api/v1/store/ - to access store
# http://127.0.0.1:5000/navyget-api/v1/store/<store_id>/item/ - to access all items in a store
# http://127.0.0.1:5000/navyget-api/v1/store/<store_id>/item/<item_id>/ - to access specific item in store
# http://127.0.0.1:5000/navyget-api/v1/store/<store_id>/service/ - to access all services in a store
# http://127.0.0.1:5000/navyget-api/v1/store/<store_id>/service/<service_id>/ - to access a specific service in a store


api_store.add_resource(Store, '/navyget-api/v1/store/', '/navyget-api/v1/store/<id>/')
api_store.add_resource(Item, '/navyget-api/v1/store/<store_id>/item/',
                       '/navyget-api/v1/store/<store_id>/item/<item_id>/')
api_store.add_resource(Service,'/navyget-api/v1/store/<store_id>/service/',
                       '/navyget-api/v1/store/<store_id>/service/<service_id>/')
