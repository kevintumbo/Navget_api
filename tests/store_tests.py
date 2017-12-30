# coding=utf-8

import json
from .base_test import BaseTestCase

store_url = '/navyget-api/v1/store/'


class TestStore(BaseTestCase):
    """ Success and Fail Tests for store creation, updating and deletion"""

    def test_successful_store_creation(self):
        """
        user can create a store
        (Post request)
        """

        self.data = {
            "store_name": "My Shop",
            "store_type": "online shop",
            "store_category": "Butchery",
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

        # make a post request and receive a success response
        response = self.client.post(store_url, data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response.status, "201 CREATED")
        self.assertIn("Success. You have created your store.", str(response.data))

    def test_creation_when_missing_shop_name(self):
        """
        User cannot create store when missing shop name
        :return:
        """
        self.data = {
            "store_name": "",
            "store_type": "online shop",
            "store_category": "Butchery",
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

        # make post request and receive a 400 response
        response = self.client.post(store_url, data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Store Name.", str(response.data))

    def test_creation_of_store_with_invalid_shop_name(self):
        """
        User cannot create store when invalid characters are in shop name
        :return:
        """

        self.data = {
            "store_name": "@jumisa&%(",
            "store_type": "online shop",
            "store_category": "Butchery",
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
        # make post request and receive a 400 response
        response = self.client.post(store_url, data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Store Name Has Invalid Characters.", str(response.data))

    def test_creation_when_missing_shop_type(self):
        """
        user cannot create store when missing shop type
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "",
            "store_category": "Butchery",
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

        # make post request and receive a 400 response
        response = self.client.post(store_url, data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Store Type.", str(response.data))

    def test_creation_when_missing_shop_category(self):
        """
        user cannot create store when missing shop category
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "online shop",
            "store_category": "",
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

        # make post request and receive a 400 response
        response = self.client.post(store_url, data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Store category.", str(response.data))

    def test_creation_when_missing_country_field(self):
        """
        user cannot create store when missing Country
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "online shop",
            "store_category": "Butchery",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "Delta Towers, 2nd floor",
                    "town_city": "Nairobi",
                    "county": "Nairobi",
                    "country": ""
                }
            ]
        }

        # make post request and receive a 400 response
        response = self.client.post(store_url, data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Country field.", str(response.data))

    def test_creation_when_missing_county_field(self):
        """
        user cannot create store when missing County
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "online shop",
            "store_category": "Butchery",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "Delta Towers, 2nd floor",
                    "town_city": "Nairobi",
                    "county": "",
                    "country": "Kenya"
                }
            ]
        }

        # make post request and receive a 400 response
        response = self.client.post(store_url, data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing County field.", str(response.data))

    def test_creation_when_missing_town_city_field(self):
        """
        User cannot create store when missing town/city field
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "online shop",
            "store_category": "Butchery",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "Delta Towers, 2nd floor",
                    "town_city": "Nairobi",
                    "county": "Nairobu",
                    "country": "Kenya"
                },
                {
                    "title": "location_2",
                    "area": "Kilimani",
                    "physical_address": "Adlife plaza",
                    "town_city": "",
                    "county": "Nairobi",
                    "country": "Kenya"
                }
            ]
        }

        # make post request and receive a 400 response
        response = self.client.post(store_url, data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing City/Town field.", str(response.data))

    def test_creation_when_missing_physical_address_field(self):
        """
        User cannot create store when missing physical_address_field
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "online shop",
            "store_category": "Butchery",
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
                    "physical_address": "",
                    "town_city": "",
                    "county": "Nairobi",
                    "country": "Kenya"
                }
            ]
        }

        # make post request and receive a 400 response
        response = self.client.post(store_url, data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing physical address field.", str(response.data))

    def test_creation_of_store_when_physical_address_has_invalid_characters(self):
        """
        User cannot create store when physical address has invalid characters
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "online shop",
            "store_category": "Butchery",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "!@#$%^&*(",
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

        # make post request and receive a 400 response
        response = self.client.post(store_url, data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Physical Address Has Invalid Characters.", str(response.data))

    def test_creation_of_duplicate_shop(self):
        """
         User cannot create a store with a shop_name that already exists
        :return:
        """
        # make post request and receive a 409 CONFLICT
        # create a store and retrieve store id
        self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        response2 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response2.status, "409 CONFLICT")
        self.assertIn("Sorry that shop name already exists. Please Pick another one.", str(response2.data))

    # GET REQUESTS FOR STORE ####################################
    def test_can_retrieve_all_the_shops(self):
        """
        User can retrieve all the stores the user has created
        :return:
        """
        response = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response.status, "201 CREATED")
        response2 = self.client.post(store_url, data=json.dumps(self.shop_one), headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        response3 = self.client.get(store_url, headers=self.my_header)
        self.assertEqual(response3.status, "200 OK")
        self.assertIn("Top Dawg Entertainment", str(response3.data))
        self.assertIn("RocNation", str(response3.data))

    def test_can_retrieve_single_store(self):
        """
        User can retrieve a single store
        :return:
        """
        # create a store and retrieve store id
        create_store = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url, data=json.dumps(self.shop_one), headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        response3 = self.client.get(store_url + store_id + '/', headers=self.my_header)
        self.assertEqual(response3.status, "200 OK")
        self.assertIn("Top Dawg Entertainment", str(response3.data))

    # def test_can_query_for_store_using_shop_name(self):
    #     """
    #     User can search for a shop and retrieve using the shop_name
    #     :return:
    #     """
    #     response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
    #     self.assertEqual(response1.status, "201 CREATED")
    #     response2 = self.client.post(store_url, data=json.dumps(self.shop_one), headers=self.my_header)
    #     self.assertEqual(response2.status, "201 CREATED")
    #     response3 = self.client.get(store_url + '?q=Top', headers=self.my_header)
    #     self.assertEqual(response3.status, "200 OK")
    #     self.assertIn("Top Dawg Entertainment", str(response3.data))

    def test_retrieve_a_store_that_does_not_exist(self):
        """
        User cannot retrieve shop that does not exist
        :return:
        """
        response = self.client.get(store_url + '5a2bc733791e4bbc9a26f7a5/', headers=self.my_header)
        self.assertEqual(response.status, "404 NOT FOUND")
        self.assertIn("Stores not found.", str(response.data))

    def test_retrieve_all_stores_that_do_not_exist(self):
        """
        User cannot get all shops that do not exist
        :return:
        """
        response = self.client.get(store_url, headers=self.my_header)
        # self.assertEqual(response.status, "404 NOT FOUND")
        self.assertIn("You have not created any store.", str(response.data))

    # PUT REQUEST TESTS FOR STORE #############################################

    def test_can_update_an_existing_shop(self):
        """
        User can update details for an existing store
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "online shop",
            "store_category": "Butchery",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "Delta Towers, 2nd floor",
                    "town_city": "Nairobi",
                    "county": "Nairobi",
                    "country": "Kenya"
                }
            ]
        }
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        store_id = json.loads(response1.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.put(store_url + store_id + '/', data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response2.status, "200 OK")
        self.assertIn("Success. You have edited My Shop\\\'s information", str(response2.data))

    def test_cannot_update_details_of_a_store_without_Id(self):
        """
        User cannot update details of a store without id
        :return:
        """
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        response2 = self.client.put(store_url, data=json.dumps(self.shop_one), headers=self.my_header)
        self.assertEqual(response2.status, "404 NOT FOUND")
        self.assertIn("Store not found.", str(response2.data))

    def test_cannot_update_details_of_store_that_does_not_exist(self):
        """
        User cannot update details of a store that does not exist
        :return:
        """
        response = self.client.put(store_url + '5a2bc733791e4bbc9a26f7a5/', data=json.dumps(self.shop_zero),
                                   headers=self.my_header)
        self.assertEqual(response.status, "404 NOT FOUND")
        self.assertIn("That Store does not exist.", str(response.data))

    def test_cannot_update_an_existing_shop_when_missing_store_name(self):
        """
        User cannot update details for an existing store when missing shop name
        :return:
        """
        self.data = {
            "store_name": "",
            "store_type": "online shop",
            "store_category": "Butchery",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "Delta Towers, 2nd floor",
                    "town_city": "Nairobi",
                    "county": "Nairobi",
                    "country": "Kenya"
                }
            ]
        }
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        store_id = json.loads(response1.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.put(store_url + store_id + '/', data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Store Name.", str(response2.data))

    def test_cannot_update_an_existing_shop_when_shop_name_has_invalid_characters(self):
        """
        User cannot update details for an existing store when shop name has invalid characters
        :return:
        """
        self.data = {
            "store_name": "!!@#$%^&&&&*",
            "store_type": "online shop",
            "store_category": "Butchery",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "Delta Towers, 2nd floor",
                    "town_city": "Nairobi",
                    "county": "Nairobi",
                    "country": "Kenya"
                }
            ]
        }
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        store_id = json.loads(response1.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.put(store_url + store_id + '/', data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Store Name Has Invalid Characters.", str(response2.data))

    def test_cannot_update_an_existing_shop_when_missing_shop_type(self):
        """
        User cannot update details for an existing store when missing shop type
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "",
            "store_category": "Butchery",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "Delta Towers, 2nd floor",
                    "town_city": "Nairobi",
                    "county": "Nairobi",
                    "country": "Kenya"
                }
            ]
        }
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        store_id = json.loads(response1.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.put(store_url + store_id + '/', data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Store Type.", str(response2.data))

    def test_cannot_update_an_existing_shop_when_missing_shop_category(self):
        """
        User cannot update details for an existing store when missing shop category
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "online shop",
            "store_category": "",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "Delta Towers, 2nd floor",
                    "town_city": "Nairobi",
                    "county": "Nairobi",
                    "country": "Kenya"
                }
            ]
        }
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        store_id = json.loads(response1.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.put(store_url + store_id + '/', data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Store category.", str(response2.data))

    def test_cannot_update_an_existing_shop_when_missing_country_field(self):
        """
        User cannot update details for an existing store when missing country field
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "physical shop",
            "store_category": "electronic",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "Delta Towers, 2nd floor",
                    "town_city": "Nairobi",
                    "county": "Nairobi",
                    "country": ""
                }
            ]
        }
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        store_id = json.loads(response1.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.put(store_url + store_id + '/', data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Country field.", str(response2.data))

    def test_cannot_update_an_existing_shop_when_missing_county_field(self):
        """
        User cannot update details for an existing store when missing county field
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "physical shop",
            "store_category": "electronic",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "Delta Towers, 2nd floor",
                    "town_city": "Nairobi",
                    "county": "",
                    "country": "Kenya"
                }
            ]
        }
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        store_id = json.loads(response1.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.put(store_url + store_id + '/', data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing County field.", str(response2.data))

    def test_cannot_update_an_existing_shop_when_missing_town_city_field(self):
        """
        User cannot update details for an existing store when missing town_city field
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "physical shop",
            "store_category": "electronic",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "Delta Towers, 2nd floor",
                    "town_city": "",
                    "county": "Nairobi",
                    "country": "Kenya"
                }
            ]
        }
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        store_id = json.loads(response1.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.put(store_url + store_id + '/', data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing City/Town field.", str(response2.data))

    def test_cannot_update_an_existing_shop_when_missing_physical_address_field(self):
        """
        User cannot update details for an existing store when missing physical_address field
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "physical shop",
            "store_category": "electronic",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "",
                    "town_city": "Nairobi",
                    "county": "Nairobi",
                    "country": "Kenya"
                }
            ]
        }
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        store_id = json.loads(response1.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.put(store_url + store_id + '/', data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing physical address field.", str(response2.data))

    def test_cannot_update_an_existing_shop_when_physical_address_field_has_invalid_characters(self):
        """
        User cannot update details for an existing store when physical_address field has invalid characters
        :return:
        """
        self.data = {
            "store_name": "My Shop",
            "store_type": "physical shop",
            "store_category": "electronic",
            "location": [
                {
                    "title": "location_1",
                    "area": "westlands",
                    "physical_address": "!@#$%^&*()",
                    "town_city": "Nairobi",
                    "county": "Nairobi",
                    "country": "Kenya"
                }
            ]
        }
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        store_id = json.loads(response1.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.put(store_url + store_id + '/', data=json.dumps(self.data), headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Physical Address Has Invalid Characters.", str(response2.data))

    # DELETE REQUEST TESTS FOR STORE #############################################

    def test_user_can_delete_store(self):
        """
        User can delete store
        :return:
        """
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        store_id = json.loads(response1.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.delete(store_url + store_id + '/', headers=self.my_header)
        self.assertEqual(response2.status, "200 OK")
        self.assertIn("You have successfully deleted the shop Top Dawg Entertainment", str(response2.data))

    def test_user_cannot_delete_store_without_id(self):
        """
        User cannot delete store without id
        :return:
        """
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        response2 = self.client.delete(store_url, headers=self.my_header)
        self.assertEqual(response2.status, "404 NOT FOUND")
        self.assertIn("Please Select an existing store", str(response2.data))

    def test_user_cannot_delete_store_that_does_not_exist(self):
        """
        User cannot delete store without that does not exist
        :return:
        """
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        response2 = self.client.delete(store_url + '5a2bc733791e4bbc9a26f7a5/', headers=self.my_header)
        self.assertEqual(response2.status, "404 NOT FOUND")
        self.assertIn("That Store does not exist.", str(response2.data))
