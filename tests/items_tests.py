# coding=utf-8

import json
from .base_test import BaseTestCase

create_store_url = '/navyget-api/v1/store/'
store_url = '/navyget-api/v1/store/'


class TestItems(BaseTestCase):
    """
    Success and Failure Tests for item creation, retrieval, updating and deletion
    """

    def test_successful_creation_of_item(self):
        """
        Shop owner can create item in store
        :return: 201 response
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))

    def test_creation_when_missing_item_name(self):
        """
        owner cannot create item when missing item name
        :return:
        """
        self.data = {
            "item_name": "",
            "item_price": "1000",
            "item_description": "The Third studio album by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue",
                "Make": "L'oreal",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Item Name.", str(response2.data))

    def test_creation_when_item_name_has_invalid_characters(self):
        """
        owner cannot create item when item name has invalid characters
        :return:
        """
        self.data = {
            "item_name": "!@#$%^",
            "item_price": "1000",
            "item_description": "The Third studio album by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue",
                "Make": "L'oreal",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Item Name Has Invalid Characters.", str(response2.data))

    def test_creation_when_missing_item_description(self):
        """
        owner cannot create item when missing item description
        :return:
        """
        self.data = {
            "item_name": "Damn",
            "item_price": "1000",
            "item_description": "",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue",
                "Make": "L'oreal",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Item Description.", str(response2.data))

    def test_creation_when_item_description_has_invalid_characters(self):
        """
        owner cannot create item when item description has invalid characters
        :return:
        """
        self.data = {
            "item_name": "Damn",
            "item_price": "1000",
            "item_description": "@#$%^&*(",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue",
                "Make": "L'oreal",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Item Description Has Invalid Characters.", str(response2.data))

    def test_creation_when_missing_item_price(self):
        """
        owner cannot create item when missing item price
        :return:
        """
        self.data = {
            "item_name": "Damn",
            "item_price": "",
            "item_description": "The Third studio album by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue",
                "Make": "L'oreal",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Item price.", str(response2.data))

    def test_creation_when_item_price_has_invalid_characters(self):
        """
        owner cannot create item when item description has invalid characters
        :return:
        """
        self.data = {
            "item_name": "Damn",
            "item_price": "$%^&",
            "item_description": "The Third studio album by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue",
                "Make": "L'oreal",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Item price Has Invalid Characters.", str(response2.data))

    def test_creation_when_missing_item_category(self):
        """
        owner cannot create item when missing item category
        :return:
        """
        self.data = {
            "item_name": "Damn",
            "item_price": "1000",
            "item_description": "The Third studio album by Kendrick Lamar",
            "item_category": "",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue",
                "Make": "L'oreal",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Item Category.", str(response2.data))

    def test_creation_when_missing_item_subcategory(self):
        """
        owner cannot create item when missing item Subcategory
        :return:
        """
        self.data = {
            "item_name": "Damn",
            "item_price": "1000",
            "item_description": "The Third studio album by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "",
            "item_attributes": {
                "Color": "Blue",
                "Make": "L'oreal",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Item Subcategory.", str(response2.data))

    def test_creation_when_item_attribute_name_is_empty(self):
        """
        store owner cannot create item if item attribute name is empty
        :return:
        """
        self.data = {
            "item_name": "Damn",
            "item_price": "1000",
            "item_description": "The Third studio album by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Live",
            "item_attributes": {
                "": "Blue",
                "Make": "Loreal",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("attribute name cannot be empty.", str(response2.data))

    def test_creation_when_item_attribute_name_has_invalid_characters(self):
        """
        store owner cannot create item if item attribute name has invalid characters
        :return:
        """
        self.data = {
            "item_name": "Damn",
            "item_price": "1000",
            "item_description": "The Third studio album by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Live",
            "item_attributes": {
                "@!@#$%^&*(": "Blue",
                "Make": "Loreal",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("@!@#$%^&*( is not a valid attribute name", str(response2.data))

    def test_creation_when_item_attribute_value_is_empty(self):
        """
        store owner cannot create item if item attribute value are empty
        :return:
        """
        self.data = {
            "item_name": "Damn",
            "item_price": "1000",
            "item_description": "The Third studio album by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Live",
            "item_attributes": {
                "Color": "Blue",
                "Make": "",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("attribute value cannot be Empty.", str(response2.data))

    def test_creation_when_item_attribute_value_has_invalid_characters(self):
        """
        store owner cannot create item if item attribute value have invalid characters
        :return:
        """
        self.data = {
            "item_name": "Damn",
            "item_price": "1000",
            "item_description": "The Third studio album by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Live",
            "item_attributes": {
                "Color": "Blue",
                "Make": "L'oreal",
                "weight": "200g",
                "expensive": "yes",
                "Height": "30cm"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("L\\\'oreal is not a valid attribute value", str(response2.data))

    def test_creation_of_duplicate_item_in_store(self):
        """
        owner cannot create duplicate item in store
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        response3 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response3.status, "409 CONFLICT")
        self.assertIn("Sorry. Damn already exists in this store.", str(response3.data))

    def test_creation_of_item_without_store_id(self):
        """
        owner cannot create shop item without shop id
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post('/navyget-api/v1/store//', data=json.dumps(self.item_zero), headers=self.my_header)
        self.assertEqual(response2.status, "404 NOT FOUND")

    def test_creation_of_item_in_store_that_does_not_exist(self):
        """
        owner cannot create item in store that does not exist
        :return:
        """
        response2 = self.client.post(store_url + '5a2bc733791e4bbc9a26f7a5/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "404 NOT FOUND")
        self.assertIn("That shop does not exist.", str(response2.data))

    # GET REQUEST TESTS #############################################################################################
    def test_can_get_all_items_from_store(self):
        """
        owner can retrieve multiple items from the store
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        # self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        response3 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.item_one),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Good Kid Mad City to the store.", str(response3.data))
        get_response = self.client.get(store_url + store_id + '/' + 'item/', headers=self.my_header)
        self.assertEqual(get_response.status, "200 OK")
        self.assertIn("Damn", str(get_response.data))
        self.assertIn("Good Kid Mad City", str(get_response.data))

    def test_cannot_get_item_from_store_without_store_id(self):
        """
        owner cannot get item from store without store id
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        get_response = self.client.get('/navyget-api/v1/store//item/', headers=self.my_header)
        self.assertEqual(get_response.status, "404 NOT FOUND")

    def test_cannot_get_item_from_store_that_does_not_exist(self):
        """
        owner cannot get item from a store that doe not exist
        :return:
        """
        get_response = self.client.get('/navyget-api/v1/store/5a2bc733791e4bbc9a26f7a5/item/', headers=self.my_header)
        self.assertEqual(get_response.status, "404 NOT FOUND")
        self.assertIn("That Store does not exist.", str(get_response.data))

    def test_cannot_get_items_that_does_not_exist(self):
        """
        Owner cannot get item that does not exist
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        get_response = self.client.get(store_url + store_id + '/item/5a2bc733791e4bbc9a26f7a5/',
                                       data=json.dumps(self.item_zero),
                                       headers=self.my_header)
        self.assertEqual(get_response.status, "404 NOT FOUND")
        self.assertIn("Item does not exist.", str(get_response.data))

    def test_can_get_get_specific_item_from_store(self):
        """
        Owner can get specific item from store
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        response3 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_one),
                                     headers=self.my_header)
        self.assertEqual(response3.status, "201 CREATED")
        self.assertIn("Success. You have added Good Kid Mad City to the store.", str(response3.data))
        item_id = json.loads(response2.data.decode('utf-8'))
        item_id = item_id['item_identifier']
        get_response = self.client.get(store_url + store_id + '/item/' + item_id + '/',
                                       headers=self.my_header)
        self.assertEqual(get_response.status, "200 OK")
        self.assertIn("Damn", str(get_response.data))

    # PUT REQUEST FOR ITEMS ############################################################################################

    def test_successful_updating_of_item_in_store(self):
        """
        Owner can successfully update an item in the store
        :return:
        """
        self.data = {
            "item_name": "Overly Dedicated",
            "item_price": "500",
            "item_description": "Mix tape by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue edit",
                "Make": "Loreal edit",
                "weight": "200g edit",
                "expensive": "yes edit",
                "Height": "30cm edit"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        item_id = json.loads(response2.data.decode('utf-8'))
        item_id = item_id['item_identifier']
        response3 = self.client.put(store_url + store_id + '/item/' + item_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "200 OK")
        self.assertIn("Overly Dedicated", str(response3.data))

    def test_cannot_update_details_of_item_that_does_not_exist(self):
        """
        Owner cannot update details of item that does not exist
        :return:
        """
        self.data = {
            "item_name": "Overly Dedicated",
            "item_price": "500",
            "item_description": "Mix tape by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue edit",
                "Make": "L'oreal edit",
                "weight": "200g edit",
                "expensive": "yes edit",
                "Height": "30cm edit"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        item_id = json.loads(response2.data.decode('utf-8'))
        item_id = item_id['item_identifier']
        response3 = self.client.put(store_url + store_id + '/item/5a2bc733791e4bbc9a26f7a5/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "404 NOT FOUND")

    def test_cannot_update_details_of_item_without_store_id(self):
        """
        store owner cannot update details of item without store id
        :return:
        """
        self.data = {
            "item_name": "Overly Dedicated",
            "item_price": "500",
            "item_description": "Mix tape by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue edit",
                "Make": "L'oreal edit",
                "weight": "200g edit",
                "expensive": "yes edit",
                "Height": "30cm edit"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        get_response = self.client.put('/navyget-api/v1/store//item/',
                                       data=json.dumps(self.data),
                                       headers=self.my_header)
        self.assertEqual(get_response.status, "404 NOT FOUND")

    def test_cannot_update_details_of_item_without_item_id(self):
        """
        Owner cannot update details of item without item id
        :return:
        """
        self.data = {
            "item_name": "Overly Dedicated",
            "item_price": "500",
            "item_description": "Mix tape by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue edit",
                "Make": "L'oreal edit",
                "weight": "200g edit",
                "expensive": "yes edit",
                "Height": "30cm edit"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        item_id = json.loads(response2.data.decode('utf-8'))
        item_id = item_id['item_identifier']
        response3 = self.client.put(store_url + store_id + '/item//',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "404 NOT FOUND")

    def test_cannot_update_an_existing_item_when_missing_item_name(self):
        """
        Owner cannot update details of item when missing item name
        :return:
        """
        self.data = {
            "item_name": "",
            "item_price": "500",
            "item_description": "Mix tape by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue edit",
                "Make": "L'oreal edit",
                "weight": "200g edit",
                "expensive": "yes edit",
                "Height": "30cm edit"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        item_id = json.loads(response2.data.decode('utf-8'))
        item_id = item_id['item_identifier']
        response3 = self.client.put(store_url + store_id + '/item/' + item_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Item Name.", str(response3.data))

    def test_cannot_update_an_existing_item_when_missing_item_price(self):
        """
        Owner cannot update details of item when missing item price
        :return:
        """
        self.data = {
            "item_name": "Overly Dedicated",
            "item_price": "",
            "item_description": "Mix tape by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue edit",
                "Make": "L'oreal edit",
                "weight": "200g edit",
                "expensive": "yes edit",
                "Height": "30cm edit"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        item_id = json.loads(response2.data.decode('utf-8'))
        item_id = item_id['item_identifier']
        response3 = self.client.put(store_url + store_id + '/item/' + item_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Item price.", str(response3.data))

    def test_cannot_update_an_existing_item_when_missing_item_description(self):
        """
        Owner cannot update details of item when missing item description
        :return:
        """
        self.data = {
            "item_name": "Overly Dedicated",
            "item_price": "500",
            "item_description": "",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue edit",
                "Make": "L'oreal edit",
                "weight": "200g edit",
                "expensive": "yes edit",
                "Height": "30cm edit"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        item_id = json.loads(response2.data.decode('utf-8'))
        item_id = item_id['item_identifier']
        response3 = self.client.put(store_url + store_id + '/item/' + item_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Item Description.", str(response3.data))

    def test_cannot_update_an_existing_item_when_missing_item_category(self):
        """
        Owner cannot update details of an item when missing item category
        :return:
        """
        self.data = {
            "item_name": "Overly Dedicated",
            "item_price": "500",
            "item_description": "Mix tape by Kendrick Lamar",
            "item_category": "",
            "item_subcategory": "Rap",
            "item_attributes": {
                "Color": "Blue edit",
                "Make": "L'oreal edit",
                "weight": "200g edit",
                "expensive": "yes edit",
                "Height": "30cm edit"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        item_id = json.loads(response2.data.decode('utf-8'))
        item_id = item_id['item_identifier']
        response3 = self.client.put(store_url + store_id + '/item/' + item_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Item Category.", str(response3.data))

    def test_cannot_update_an_existing_item_when_missing_item_subcategory(self):
        """
        Owner cannot update details of an item when missing item Subcategory
        :return:
        """
        self.data = {
            "item_name": "Overly Dedicated",
            "item_price": "500",
            "item_description": "Mix tape by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "",
            "item_attributes": {
                "Color": "Blue edit",
                "Make": "L'oreal edit",
                "weight": "200g edit",
                "expensive": "yes edit",
                "Height": "30cm edit"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        item_id = json.loads(response2.data.decode('utf-8'))
        item_id = item_id['item_identifier']
        response3 = self.client.put(store_url + store_id + '/item/' + item_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Item Subcategory.", str(response3.data))

    def test_cannot_update_item_attributes_name_with_invalid_characters(self):
        """
        Owner cannot update item attributes if name has invalid characters
        :return:
        """
        self.data = {
            "item_name": "Overly Dedicated",
            "item_price": "500",
            "item_description": "Mix tape by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "color": "Blue edit",
                "Make": "Loreal edit",
                "@#$%^&*(": "200g edit",
                "expensive": "yes edit",
                "Height": "30cm edit"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        item_id = json.loads(response2.data.decode('utf-8'))
        item_id = item_id['item_identifier']
        response3 = self.client.put(store_url + store_id + '/item/' + item_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("@#$%^&*( is not a valid attribute name", str(response3.data))

    def test_cannot_update_item_attributes_when_attribute_name_is_empty(self):
        """
        Store owner cannot update item attributes when attribute name is empty
        :return:
        """
        self.data = {
            "item_name": "Overly Dedicated",
            "item_price": "500",
            "item_description": "Mix tape by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "color": "Blue edit",
                "Make": "Loreal edit",
                "": "200g edit",
                "expensive": "yes edit",
                "Height": "30cm edit"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        item_id = json.loads(response2.data.decode('utf-8'))
        item_id = item_id['item_identifier']
        response3 = self.client.put(store_url + store_id + '/item/' + item_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("attribute name cannot be Empty.", str(response3.data))

    def test_cannot_update_item_attributes_value_with_invalid_characters(self):
        """
        Owner cannot update item attributes if name has invalid characters
        :return:
        """
        self.data = {
            "item_name": "Overly Dedicated",
            "item_price": "500",
            "item_description": "Mix tape by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "color": "Blue edit",
                "Make": "Loreal edit",
                "@#$%^&*(": "!@#$%^&*()",
                "expensive": "yes edit",
                "Height": "30cm edit"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        item_id = json.loads(response2.data.decode('utf-8'))
        item_id = item_id['item_identifier']
        response3 = self.client.put(store_url + store_id + '/item/' + item_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("@#$%^&*( is not a valid attribute name", str(response3.data))

    def test_cannot_update_item_attributes_when_attribute_value_is_empty(self):
        """
        Store owner cannot update item attributes when attribute name is empty
        :return:
        """
        self.data = {
            "item_name": "Overly Dedicated",
            "item_price": "500",
            "item_description": "Mix tape by Kendrick Lamar",
            "item_category": "Music",
            "item_subcategory": "Rap",
            "item_attributes": {
                "color": "Blue edit",
                "Make": "Loreal edit",
                "weight": "",
                "expensive": "yes edit",
                "Height": "30cm edit"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        item_id = json.loads(response2.data.decode('utf-8'))
        item_id = item_id['item_identifier']
        response3 = self.client.put(store_url + store_id + '/item/' + item_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("attribute value cannot be Empty.", str(response3.data))

    # DELETE REQUEST FOR ITEMS ########################################################################################

    def test_successful_deletion_of_item_in_store(self):
        """
        Store owner can successfully delete an item from the store
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        item_id = json.loads(response2.data.decode('utf-8'))
        item_id = item_id['item_identifier']
        response3 = self.client.delete(store_url + store_id + '/item/' + item_id + '/',
                                       headers=self.my_header)
        self.assertEqual(response3.status, "200 OK")
        self.assertIn("You have successfully deleted Damn from the store Top Dawg Entertainment", str(response3.data))

    def test_user_cannot_delete_item_without_store_id(self):
        """
        Store owner cannot delete an item when store id is missing
        :return:
        """
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        response2 = self.client.delete(store_url, headers=self.my_header)
        self.assertEqual(response2.status, "404 NOT FOUND")
        self.assertIn("Please Select an existing store", str(response2.data))

    def test_cannot_delete_item_in_store_that_does_not_exist(self):
        """
        Store owner cannot delete item in store that does not exist
        :return:
        """
        response1 = self.client.post(store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(response1.status, "201 CREATED")
        response2 = self.client.delete(store_url + '5a2bc733791e4bbc9a26f7a5/item/', headers=self.my_header)
        self.assertEqual(response2.status, "404 NOT FOUND")
        self.assertIn("That Store does not exist.", str(response2.data))

    def test_cannot_delete_item_without_item_id(self):
        """
        store owner cannot delete item without the item id
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        # self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        response3 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.item_one),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Good Kid Mad City to the store.", str(response3.data))
        get_response = self.client.delete(store_url + store_id + '/item//', headers=self.my_header)
        self.assertEqual(get_response.status, "404 NOT FOUND")

    def test_cannot_delete_item_that_does_not_exist(self):
        """
        Store owner cannot delete item that does not exist
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data.decode('utf-8'))
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.item_zero),
                                     headers=self.my_header)
        # self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Damn to the store.", str(response2.data))
        response3 = self.client.post(store_url + store_id + '/' + 'item/',
                                     data=json.dumps(self.item_one),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added Good Kid Mad City to the store.", str(response3.data))
        get_response = self.client.delete(store_url + store_id + '/item/5a2bc733791e4bbc9a26f7a5/',
                                          headers=self.my_header)
        self.assertEqual(get_response.status, "404 NOT FOUND")
