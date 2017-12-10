# coding=utf-8

import json
from .base_test import BaseTestCase

create_store_url = '/navyget-api/v1/store/'
store_url = '/navyget-api/v1/store/'


class TestServices(BaseTestCase):
    """
    Success and Failure Tests for service creation, retrieval, updating and deletion
    """

    def test_successful_creation_of_service(self):
        """
        Store owner can create service in store
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))

    def test_creation_when_missing_service_name(self):
        """
        store owner cannot create service when missing service name
        :return:
        """
        self.data = {
            "service_name": "",
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

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Service Name.", str(response2.data))

    def test_creation_when_service_name_has_invalid_characters(self):
        """
        store owner cannot create service when service name has invalid characters
        :return:
        """
        self.data = {
            "service_name": "@#$%^&*((",
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

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Service Name Has Invalid Characters.", str(response2.data))

    def test_creation_when_missing_service_price(self):
        """
        store owner cannot create service when missing service price
        :return:
        """
        self.data = {
            "service_name": "Live at the yard",
            "service_price": "",
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

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Service price.", str(response2.data))

    def test_creation_when_missing_service_description(self):
        """
        store owner cannot create service when missing service description
        :return:
        """

        self.data = {
            "service_name": "Live at the yard",
            "service_price": "5000",
            "service_description": "",
            "service_category": "Music",
            "service_subcategory": "Live",
            "service_attributes": {
                "duration": "as long ",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Service Description.", str(response2.data))

    def test_creation_when_service_description_has_invalid_characters(self):
        """
        store owner cannot create service when service description has invalid characters
        :return:
        """
        self.data = {
            "service_name": "Live at the yard",
            "service_price": "5000",
            "service_description": "!@#$%^&*(((",
            "service_category": "Music",
            "service_subcategory": "Live",
            "service_attributes": {
                "duration": "as long ",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Service Description Has Invalid Characters.", str(response2.data))

    def test_creation_when_missing_service_category(self):
        """
        store owner cannot create service when missing service category
        :return:
        """
        self.data = {
            "service_name": "Live at the yard",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the yard",
            "service_category": "",
            "service_subcategory": "Live",
            "service_attributes": {
                "duration": "as long ",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Service Category", str(response2.data))

    def test_creation_when_missing_service_subcategory(self):
        """
        store owner cannot create service when missing service subcategory
        :return:
        """
        self.data = {
            "service_name": "Live at the yard",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the yard",
            "service_category": "Music",
            "service_subcategory": "",
            "service_attributes": {
                "duration": "as long ",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Service Subcategory", str(response2.data))

    def test_creation_when_service_attributes_name_is_empty(self):
        """
        store owner cannot create service if service attribute name is empty
        :return:
        """
        self.data = {
            "service_name": "Live at the yard",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the yard",
            "service_category": "Music",
            "service_subcategory": "Live",
            "service_attributes": {
                "": "as long ",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("attribute name cannot be empty.", str(response2.data))

    def test_creation_when_service_attributes_name_has_invalid_characters(self):
        """
        store owner cannot create service if attribute name has invalid characters
        :return:
        """
        self.data = {
            "service_name": "Live at the yard",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the yard",
            "service_category": "Music",
            "service_subcategory": "Live",
            "service_attributes": {
                "!@#$%^&": "as long ",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("@#$%^& is not a valid attribute name", str(response2.data))

    def test_creation_when_service_attributes_value_is_empty(self):
        """
        store owner cannot create service if service attribute value is empty
        :return:
        """
        self.data = {
            "service_name": "Live at the yard",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the yard",
            "service_category": "Music",
            "service_subcategory": "Live",
            "service_attributes": {
                "duration": "",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("attribute value cannot be Empty.", str(response2.data))

    def test_creation_when_service_attributes_value_has_invalid_characters(self):
        """
        store owner cannot create service if attributes value has invalid characters
        :return:
        """
        self.data = {
            "service_name": "Live at the yard",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the yard",
            "service_category": "Music",
            "service_subcategory": "Live",
            "service_attributes": {
                "duration": "!!@#$%^&*",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }

        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.data),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "400 BAD REQUEST")
        self.assertIn("!!@#$%^&* is not a valid attribute value", str(response2.data))

    def test_creation_of_duplicate_service_in_store(self):
        """
        store owner cannot create service with duplicate name
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        response3 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response3.status, "409 CONFLICT")
        self.assertIn("Sorry. Live at the yard already exists in this store.", str(response3.data))

    def test_creation_of_service_in_store_without_store_id(self):
        """
        store owner cannot create service in store without store id
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post('/navyget-api/v1/store//',
                                     data=json.dumps(self.service_zero), headers=self.my_header)
        self.assertEqual(response2.status, "404 NOT FOUND")

    def test_creation_of_service_in_store_that_does_not_exist(self):
        """
        store owner cannot create service in store that does that does not exist
        :return:
        """
        response2 = self.client.post(store_url + '5a2bc733791e4bbc9a26f7a5/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "404 NOT FOUND")
        self.assertIn("That Store does not exist.", str(response2.data))

    # GET REQUEST TESTS ###############################################################################################
    def test_can_get_all_services_from_store(self):
        """
        store owner can retrieve multiple/all services from the store
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        response3 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_one),
                                     headers=self.my_header)
        self.assertEqual(response3.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the bush  to the store.", str(response3.data))
        get_response = self.client.get(store_url + store_id + '/service/', headers=self.my_header)
        self.assertEqual(get_response.status, "200 OK")
        self.assertIn("Live at the yard", str(get_response.data))
        self.assertIn("Live at the bush", str(get_response.data))

    def test_cannot_get_service_from_store_without_store_id(self):
        """
        store owner cannot retrieve service from store without store id
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        get_response = self.client.get('/navyget-api/v1/store//service/', headers=self.my_header)
        self.assertEqual(get_response.status, "404 NOT FOUND")

    def test_cannot_get_service_from_store_that_does_not_exist(self):
        """
        store owner cannot retrieve service from from store that does not exist
        :return:
        """
        get_response = self.client.get('/navyget-api/v1/store/5a2bc733791e4bbc9a26f7a5/service/', headers=self.my_header)
        self.assertEqual(get_response.status, "404 NOT FOUND")
        self.assertIn("That Store does not exist.", str(get_response.data))

    def test_cannot_get_service_that_does_not_exist(self):
        """
        store owner cannot retrieve service that does not exist
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        get_response = self.client.get(store_url + store_id + '/service/5a2bc733791e4bbc9a26f7a5/',
                                       data=json.dumps(self.service_zero),
                                       headers=self.my_header)
        self.assertEqual(get_response.status, "404 NOT FOUND")
        self.assertIn("Service does not exist.", str(get_response.data))

    def test_can_get_specific_service_from_store(self):
        """
        store owner can retrieve specific service from store
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        response3 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_one),
                                     headers=self.my_header)
        self.assertEqual(response3.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the bush  to the store.", str(response3.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        get_response = self.client.get(store_url + store_id + '/service/' + service_id + '/', headers=self.my_header)
        self.assertEqual(get_response.status, "200 OK")
        self.assertIn("Live at the yard", str(get_response.data))

    # PUT REQUEST FOR SERVICES ########################################################################################

    def test_successful_updating_of_service_in_store(self):
        """
        store owner can successfully update an service in the store
        :return:
        """
        self.data = {
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
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        response3 = self.client.put(store_url + store_id + '/service/' + service_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "200 OK")
        self.assertIn("Live at the shop", str(response3.data))

    def test_cannot_update_details_of_service_that_does_not_exist(self):
        """
        store owner cannot update details of service that does not exist
        :return:
        """
        self.data = {
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
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        response3 = self.client.put(store_url + store_id + '/service/5a2bc733791e4bbc9a26f7a5/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "404 NOT FOUND")

    def test_cannot_update_details_of_service_without_store_id(self):
        """
        store owner cannot update details of service without store id
        :return:
        """
        self.data = {
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
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        self.assertEqual(create_store.status, "201 CREATED")
        get_response = self.client.put('/navyget-api/v1/store//service/',
                                       data=json.dumps(self.data),
                                       headers=self.my_header)
        self.assertEqual(get_response.status, "404 NOT FOUND")

    def test_cannot_update_details_of_service_without_service_id(self):
        """
        store owner cannot update details of service without service id
        :return:
        """
        self.data = {
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
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        response3 = self.client.put(store_url + store_id + '/service//',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "404 NOT FOUND")

    def test_cannot_update_an_existing_service_when_missing_service_name(self):
        """
        Owner cannot update details of service when missing service name
        :return:
        """
        self.data = {
            "service_name": "",
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
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        response3 = self.client.put(store_url + store_id + '/service/' + service_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Service Name.", str(response3.data))

    def test_cannot_update_an_existing_service_when_missing_service_price(self):
        """
        Owner cannot update details of service when missing service price
        :return:
        """
        self.data = {
            "service_name": "Live at the shop",
            "service_price": "",
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
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        response3 = self.client.put(store_url + store_id + '/service/' + service_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Service price.", str(response3.data))

    def test_cannot_update_an_existing_service_when_missing_service_description(self):
        """
        Owner cannot update details of service when missing service description
        :return:
        """
        self.data = {
            "service_name": "Live at the yard",
            "service_price": "5000",
            "service_description": "",
            "service_category": "Music",
            "service_subcategory": "Live",
            "service_attributes": {
                "duration": "as long ",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        response3 = self.client.put(store_url + store_id + '/service/' + service_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Service Description.", str(response3.data))

    def test_cannot_update_an_existing_service_when_missing_service_category(self):
        """
        Owner cannot update details of an service when missing service category
        :return:
        """
        self.data = {
            "service_name": "Live at the shop",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the shop",
            "service_category": "",
            "service_subcategory": "Live",
            "service_attributes": {
                "duration": "as long ",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        response3 = self.client.put(store_url + store_id + '/service/' + service_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Service Category.", str(response3.data))

    def test_cannot_update_an_existing_service_when_missing_service_subcategory(self):
        """
        Owner cannot update details of an service when missing service Subcategory
        :return:
        """
        self.data = {
            "service_name": "Live at the shop",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the shop",
            "service_category": "Music",
            "service_subcategory": "",
            "service_attributes": {
                "duration": "as long ",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        response3 = self.client.put(store_url + store_id + '/service/' + service_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Service Subcategory.", str(response3.data))

    def test_updating_when_service_attributes_name_is_empty(self):
        """
        store owner cannot update service if service attribute name is empty
        :return:
        """
        self.data = {
            "service_name": "Live at the shop",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the shop",
            "service_category": "Music",
            "service_subcategory": "Live",
            "service_attributes": {
                "": "as long ",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        response3 = self.client.put(store_url + store_id + '/service/' + service_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("attribute name cannot be empty.", str(response3.data))

    def test_updating_when_service_attributes_name_has_invalid_characters(self):
        """
        store owner cannot update service if attribute name has invalid characters
        :return:
        """
        self.data = {
            "service_name": "Live at the shop",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the shop",
            "service_category": "Music",
            "service_subcategory": "Live",
            "service_attributes": {
                "!@#$%^&*": "as long ",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        response3 = self.client.put(store_url + store_id + '/service/' + service_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("!@#$%^&* is not a valid attribute name", str(response3.data))

    def test_updating_when_service_attributes_value_is_empty(self):
        """
        store owner cannot update service if service attribute value is empty
        :return:
        """
        self.data = {
            "service_name": "Live at the shop",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the shop",
            "service_category": "Music",
            "service_subcategory": "Live",
            "service_attributes": {
                "duration": "",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        response3 = self.client.put(store_url + store_id + '/service/' + service_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("attribute value cannot be Empty.", str(response3.data))

    def test_updating_when_service_attributes_value_has_invalid_characters(self):
        """
        store owner cannot update service if attributes value has invalid characters
        :return:
        """
        self.data = {
            "service_name": "Live at the shop",
            "service_price": "5000",
            "service_description": "See Kendrick perform live at the shop",
            "service_category": "Music",
            "service_subcategory": "Live",
            "service_attributes": {
                "duration": "!@#$%^&",
                "width": "20",
                "length": "20",
                "height": "20"
            }
        }
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        response3 = self.client.put(store_url + store_id + '/service/' + service_id + '/',
                                    data=json.dumps(self.data),
                                    headers=self.my_header)
        self.assertEqual(response3.status, "400 BAD REQUEST")
        self.assertIn("!@#$%^& is not a valid attribute value", str(response3.data))

    # DELETE REQUEST FOR SERVICES  ####################################################################################

    def test_successful_deletion_of_service_in_store(self):
        """
        Store owner can successfully delete an service from the store
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        get_response = self.client.delete(store_url + store_id + '/service/' + service_id + '/', headers=self.my_header)
        self.assertEqual(get_response.status, "200 OK")
        self.assertIn("You have successfully deleted Live at the yard the store Top Dawg Entertainment",
                      str(get_response.data))

    def test_user_cannot_delete_service_in_store_that_does_not_exist(self):
        """
        Store owner cannot delete a service in a store that does not exist
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        get_response = self.client.delete(store_url+ '5a2bc733791e4bbc9a26f7a5/service/' + service_id + '/',
                                          headers=self.my_header)
        self.assertEqual(get_response.status, "404 NOT FOUND")
        self.assertIn("That Store does not exist.", str(get_response.data))

    def test_cannot_delete_service_without_store_id(self):
        """
        Store owner cannot delete a service without store id
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        get_response = self.client.delete(store_url + '/service/' + service_id + '/', headers=self.my_header)
        self.assertEqual(get_response.status, "404 NOT FOUND")

    def test_cannot_delete_service_without_service_id(self):
        """
        store owner cannot delete service without the service id
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        service_id = json.loads(response2.data)
        service_id = service_id['service_identifier']
        get_response = self.client.delete(store_url + store_id + '/service//', headers=self.my_header)
        self.assertEqual(get_response.status, "404 NOT FOUND")

    def test_cannot_delete_service_that_does_not_exist(self):
        """
        Store owner cannot delete service that does not exist
        :return:
        """
        create_store = self.client.post(create_store_url, data=json.dumps(self.shop_zero), headers=self.my_header)
        store_id = json.loads(create_store.data)
        store_id = json.loads(store_id['store_id'])
        store_id = store_id['$oid']
        response2 = self.client.post(store_url + store_id + '/service/',
                                     data=json.dumps(self.service_zero),
                                     headers=self.my_header)
        self.assertEqual(response2.status, "201 CREATED")
        self.assertIn("Success. You have added a new Service Live at the yard to the store.", str(response2.data))
        get_response = self.client.delete(store_url + store_id + '/service/5a2bc733791e4bbc9a26f7a5/',
                                          headers=self.my_header)
        self.assertEqual(get_response.status, "404 NOT FOUND")
        self.assertIn("Service does not exist", str(get_response.data))
