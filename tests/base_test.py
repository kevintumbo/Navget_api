from app import create_app, db
import json

import unittest

register_url = '/navyget-api/v1/auth/register'
login_url = '/navyget-api/v1/auth/login'


class BaseTestCase(unittest.TestCase):
    """ Base Test cases for running tests """

    def setUp(self):
        """ creates Base test """

        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()

        self.user_zero = {
            "first_name": "kendrick",
            "last_name": "lamar",
            "username": "kungfukenny",
            "email": "kdot@gmail.com",
            "password": "password1234"
        }

        self.shop_zero = {
            "shop_name": "Top Dawg Entertainment",
            "shop_type": "online shop",
            "shop_category": "music",
            "country": "Kenya",
            "county": "Nairobi",
            "town_city": "Nairobi",
            "physical_address": "Lantana Flats",
            "owner_id": 1
        }

        self.shop_one = {
            "shop_name": "RocNation",
            "shop_type": "online shop",
            "shop_category": "music",
            "country": "Kenya",
            "county": "Nairobi",
            "town_city": "Nairobi",
            "physical_address": "Mountain View",
            "owner_id": 1
        }

        self.item_zero = {
            "item_name": "Damn",
            "item_price": "1000",
            "item_description": "Third studio album by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "owner_id": 1,
            "shop_id": 1
        }

        self.service_zero = {
            "service_name": "Live at the yard",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the yard",
            "service_category": "Music",
            "service_subcategory": "Live",
            "owner_id": 1,
            "shop_id": 1
        }

        with self.app.app_context():

            db.create_all()
            # register and log in user
            self.client.post(register_url, data=json.dumps(self.user_zero), headers={"Content-Type": "application/json"})
            self.user_login = {
                "email": "kdot@gmail.com",
                "password": "password1234"
            }
            base_result = self.client.post(login_url, data=json.dumps(self.user_login), headers={"Content-Type": "application/json"})
            access_token = json.loads(base_result.data.decode())['access_token']
            self.my_header = {'Authorization': 'Token ' + access_token,
                              'Content-Type': 'application/json',
                             }
    def tearDown(self):
        """ removes resources once tests have run """
        with self.app.app_context():

            db.session.remove()
            db.drop_all()