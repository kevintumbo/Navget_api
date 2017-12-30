from app import create_app
from mongoengine import connect
import json

import unittest

user_register_url = '/navyget-api/v1/auth/user-register'
business_register_url = '/navyget-api/v1/auth/business-register'
login_url = '/navyget-api/v1/auth/login'
create_store_url = '/navyget-api/v1/store/'


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
            "store_name": "Top Dawg Entertainment",
            "store_type": "physical shop",
            "store_category": "music",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "Delta Towers, 2nd floor",
                    "town_city": "Nairobi",
                    "county": "Nairobi",
                    "country": "Kenya"
                },
                {
                    "title": "location_2",
                    "area": "Kilimani",
                    "physical_address": "Adlife plaza",
                    "town_city": "Nairobi",
                    "county": "Nairobi",
                    "country": "Kenya"
                }
            ]
        }

        self.shop_one = {
            "store_name": "RocNation",
            "store_type": "online shop",
            "store_category": "music",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "Delta Towers, 2nd floor",
                    "town_city": "Nairobi",
                    "county": "Nairobi",
                    "country": "Kenya"
                },
                {
                    "title": "location_2",
                    "area": "Kilimani",
                    "physical_address": "Adlife plaza",
                    "town_city": "Nairobi",
                    "county": "Nairobi",
                    "country": "Kenya"
                }
            ]
        }

        self.item_zero = {
            "item_name": "Damn",
            "item_price": "1000",
            "item_description": "The Third studio album by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue",
                "Make": "Loreal",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        self.item_one = {
            "item_name": "Good Kid Mad City",
            "item_price": "1000",
            "item_description": "The First studio album by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue",
                "Make": "Loreal",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        self.item_two = {
            "item_name": "To pimp a Butterfly",
            "item_price": "1000",
            "item_description": "The Second studio album by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue",
                "Make": "Loreal",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        self.service_zero = {
            "service_name": "Live at the yard",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the yard",
            "service_category": "Music",
            "service_subcategory": "Live",
            "service_attributes": {
                "duration": "as long ",
                "width": "20",
                "length": "20",
                "height": "20"
                }
        }

        self.service_one = {
            "service_name": "Live at the bush ",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the bush",
            "service_category": "Music",
            "service_subcategory": "Live",
            "service_attributes": {
                "duration": "as long ",
                "width": "20",
                "length": "20",
                "height": "20"
                }
        }

        self.service_two = {
            "service_name": "Live at the shop",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the shop",
            "service_category": "Music",
            "service_subcategory": "Live",
            "service_attributes": {
                "duration": "as long ",
                "width": "20",
                "length": "20",
                "height": "20"
                }
        }

        with self.app.app_context():
            db = connect('test_navy_api')

            # register and log in user
            response = self.client.post(user_register_url, data=json.dumps(self.user_zero), headers={"Content-Type": "application/json"})
            self.assertEqual(response.status, "201 CREATED")
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
            db = connect('test_navy_api')
            db.drop_database('test_navy_api')
