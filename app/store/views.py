from flask import g, url_for, jsonify
import re
from flask_restful import Resource, Api, reqparse
from flask_httpauth import HTTPTokenAuth
from . import store_blueprint
from ..models import User, Shops

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


class Store(Resource):
    """
    Api resource for handling the store
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('shop_name', required=True, help="Error. Missing Shop Name.")
        self.parser.add_argument('shop_type', required=True, help="Error. Missing Shop Type.")
        self.parser.add_argument('shop_category', required=True, help="Error. Missing Shop Category.")
        self.parser.add_argument('country', required=True, help="Error. Missing Country Field.")
        self.parser.add_argument('county', required=True, help="Error. Missing county Field.")
        self.parser.add_argument('town_city', required=True, help="Error. Missing town/city Field.")
        self.parser.add_argument('physical_address', required=True, help="Error. Missing Physical address Field.")
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

        # confirm shop name value exists and is of valid format
        shop_name = args['shop_name']
        if not shop_name:
            response = {
                'message': 'Error. Missing Shop Name.'
            }
            # return a response notifying them that shop name is  missing
            return response, 400

        check_shop_name = re.match('^[a-z A-Z0-9_.-]+$', shop_name)
        if check_shop_name is None:
            response = {
                'message': 'Error. Shop Name Has Invalid Characters.'
            }
            # return a response notifying the user that credentials shop name is invalid
            return response, 400

        # Confirm shop type exists
        shop_type = args['shop_type']
        if not shop_type:
            response = {
                'message': 'Error. Missing Shop Type.'
            }
            # return a response notifying them that shop Type is missing
            return response, 400

        # confirm shop category exists
        shop_category = args['shop_category']
        if not shop_category:
            response = {
                'message': 'Error. Missing shop category.'
            }
            # return a response notifying them that shop Category is missing
            return response, 400

        # confirm country field exists
        country = args['country']
        if not country:
            response = {
                'message': 'Error. Missing Country field.'
            }
            # return a response notifying them that Country is missing
            return response, 400

        # confirm county field exists
        county = args['county']
        if not county:
            response = {
                'message': 'Error. Missing County field.'
            }
            # return a response notifying them that county is missing
            return response, 400

        # confirm town/city field exists
        town_city = args['town_city']
        if not town_city:
            response = {
                'message': 'Error. Missing City/Town field.'
            }

            # return a response notifying them that City/Town field is missing
            return response, 400

        # confirm  physical address exists
        physical_address = args['physical_address']
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

        # Query to see if shop name already exists
        shop_name = Shops.query.filter_by(shop_name=shop_name,owner_id=g.user.id).first()

        if not shop_name:
            # if shop name does not exist, we can create the shop.
            try:
                shop = Shops(
                             shop_name=args['shop_name'],
                             shop_type=args['shop_type'],
                             shop_category=args['shop_category'],
                             country=args['country'],
                             county=args['county'],
                             town_city=args['town_city'],
                             physical_address=args['physical_address'],
                             owner_id=g.user.id)
                shop.save()

                response = {
                    'message': 'Success. You have created your store.'
                }

                return response, 201
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
        GET request to retrieve list of all shops owned by the user
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
            single_shop = Shops.query.filter_by(owner_id=g.user.id, id=id).filter(Shops.shop_name.like('%{}%'.format(q))).first()
            if not single_shop:
                response = {
                    'message': 'Shop not found.'
                }
                return response, 404

            response = jsonify({
                "shop_id": single_shop.id,
                "shop_name": single_shop.shop_name,
                "shop_type": single_shop.shop_type,
                "shop_category": single_shop.shop_category,
                "physical_address": single_shop.physical_address,
                "town_city": single_shop.town_city,
                "county": single_shop.county,
                "country": single_shop.country,
                "date_created": single_shop.date_created,
                "date_modified": single_shop.date_modified
            })
            response.status_code = 200
            return response

        # Query to see if shop name already exists
        all_shops = Shops.query.filter_by(owner_id=g.user.id).filter(Shops.shop_name.like('%{}%'.format(q))).paginate(
                            int(page_no), int(limit))
        if not all_shops.items:
            response = {
                'message': 'You have not created any store.'
            }
            return response, 404

        response = jsonify({
            'shops': [
                {
                    "shop_id": shop.id,
                    "shop_name": shop.shop_name,
                    "shop_type": shop.shop_type,
                    "shop_category": shop.shop_category,
                    "physical_address": shop.physical_address,
                    "town_city": shop.town_city,
                    "county": shop.county,
                    "country": shop.country,
                    "date_created": shop.date_created,
                    "date_modified": shop.date_modified
                } for shop in all_shops.items
            ],
            'next': url_for(args.endpoint, page_no=all_shops.next_num, limit=limit,
                            _external=True) if all_shops.has_next else None,
            'prev': url_for(args.endpoint, page_no=all_shops.prev_num, limit=limit,
                            _external=True) if all_shops.has_prev else None,
        })
        response.status_code = 200
        return response

    @auth.login_required
    def put(self, id=None):
        """
        PUT request to edit details of a shop
        :return: response
        """
        if not id:
            response = {
                'message': 'Shop not found.'
            }
            return response, 404

        # query the database for the shop with the id
        shop = Shops.query.filter_by(owner_id=g.user.id, id=id).first()
        if not shop:
            response = {
                'message': 'That shop does not exist.'
            }
            return response, 404

        args = self.parser.parse_args()

        # confirm shop name value exists and is of valid format
        shop_name = args['shop_name']
        if not shop_name:
            response = {
                'message': 'Error. Missing Shop Name.'
            }
            # return a response notifying them that shop name is  missing
            return response, 400

        check_shop_name = re.match('^[a-z A-Z0-9_.-]+$', shop_name)
        if check_shop_name is None:
            response = {
                'message': 'Error. Shop Name Has Invalid Characters.'
            }
            # return a response notifying the user that credentials shop name is invalid
            return response, 400

        # Confirm shop type exists
        shop_type = args['shop_type']
        if not shop_type:
            response = {
                'message': 'Error. Missing Shop Type.'
            }
            # return a response notifying them that shop Type is missing
            return response, 400

        # confirm shop category exists
        shop_category = args['shop_category']
        if not shop_category:
            response = {
                'message': 'Error. Missing shop category.'
            }
            # return a response notifying them that shop Category is missing
            return response, 400

        # confirm country field exists
        country = args['country']
        if not country:
            response = {
                'message': 'Error. Missing Country field.'
            }
            # return a response notifying them that Country is missing
            return response, 400

        # confirm county field exists
        county = args['county']
        if not county:
            response = {
                'message': 'Error. Missing County field.'
            }
            # return a response notifying them that county is missing
            return response, 400

        # confirm town/city field exists
        town_city = args['town_city']
        if not town_city:
            response = {
                'message': 'Error. Missing City/Town field.'
            }

            # return a response notifying them that City/Town field is missing
            return response, 400

        # confirm  physical address exists
        physical_address = args['physical_address']
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
        shop.shop_name = shop_name
        shop.shop_type = shop_type
        shop.shop_category = shop_category
        shop.country = country
        shop.county = county
        shop.town_city = town_city
        shop.physical_address = physical_address
        shop.save()

        response = {
            "shop_id": shop.id,
            "shop_name": shop.shop_name,
            "shop_type": shop.shop_type,
            "shop_category": shop.shop_category,
            "physical_address": shop.physical_address,
            "town_city": shop.town_city,
            "county": shop.county,
            "country": shop.country,
            "message": "Success. You have edited {}'s information.".format(shop.shop_name)
        }

        return response, 200

    @auth.login_required
    def delete(self, id=None):
        """
        Delete Request to delete shop details
        :return:
        """
        if not id:
            response = {
                "message": "Please Select an existing shop"
            }
            return response, 404

        # query to see if shop exists
        shop = Shops.query.filter_by(owner_id=g.user.id, id=id).first()
        if not shop:
            response = {
                "message": "That shop does not exist."
            }
            return response, 404
        shop_name = shop.shop_name
        shop.delete()
        response = {
            "message": "You have successfully deleted the shop {}".format(shop_name)
        }
        return response, 200

# make resource accessible to the system
# http://127.0.0.1:5000/navyget-api/v1/store/


api_store.add_resource(Store, '/navyget-api/v1/store/', '/navyget-api/v1/store/<int:id>/')
