from app import create_app, db
from app.models import User, Shops, Items, Services

import json
import unittest

class BaseTestCase(unittest.TestCase):
    """ Base Test cases for running tests """

    def setUp(self):
        """ creates basetest """

        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()

        self.user_zero = {
            "first_name" : "kendrick",
            "last_name" : "lamar",
            "username" : "kung-fukenny",
            "email" : "kdot@gmail.com",
            "password" : "password1234"
        }

        self.shop_zero = {
            "shop_name" : "Top Dawg Entertainment",
            "shop_type" : "online shop",
            "shop_category" : "music",
            "country" : "Kenya",
            "county" : "Nairobi",
            "town_city" : "Nairobi",
            "physical_address" : "Lantana Flats",
            "owner_id" : 1
        }

        self.item_zero = {
            "item_name" : "Damn",
            "item_price" : "1000",
            "item_description" : "Third studio album by Kendrick Lamar",
            "item_category" : "Music",
            "item_subcategory" : "Rap",
            "owner_id" : 1,
            "shop_id" : 1
        }

        self.service_zero = {
            "service_name" : "Live at the yard",
            "service_price" : "5000",
            "service_description" : "See Kendrick perform live at the yard",
            "service_category" : "Music",
            "service_subcategory" : "Live",
            "owner_id" : 1,
            "shop_id" : 1
        }

        with self.app.app_context():

            db.create_all()
        
    def tearDown(self):
        """ removes resources once tests have run """
        with self.app.app_context():

            db.session.remove()
            db.drop_all()
