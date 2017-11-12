import json
from .base_test import BaseTestCase

register_url = '/navyget-api/v1/auth/register'
login_url = '/navyget-api/v1/auth/login'


class TestAuthentication(BaseTestCase):
    """ Success and Fail Tests for user authentication log in and logout """

    def test_successful_user_registration(self):
        """
        successfully creates user
        (Post request)
        """

        self.data = {
            "first_name": "kyle",
            "last_name": "walker",
            "username": "kyliewalker",
            "email": "kylie@gmail.com",
            "password": "password1234"
        }

        # make a post request and receive a success response
        response = self.client.post(register_url, data=json.dumps(self.data), headers={"Content-Type": "application/json"})
        self.assertEqual(response.status, "201 CREATED")
        self.assertIn("Success. You have registered. You can Log in", str(response.data))

    def test_registration_when_missing_first_name(self):
        """
        fails to creates user due to missing first name
        (Post Request)
        """

        self.data = {
            "first_name" : "",
            "last_name" : "walker",
            "username" : "kyliewalker",
            "email" : "kylie@gmail.com",
            "password" : "password1234"
        }

        # make a post request and recieve a failure response
        response = self.client.post(register_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing First Name", str(response.data))

    def test_registration_when_missing_last_name(self):
        """
        fails to creates user due to missing last name
        (Post Request)
        """

        self.data = {
            "first_name" : "paul",
            "username" : "paulie_pogba",
            "email" : "paulie_pogba@gmail.com",
            "password" : "password1234"
        }

        # make a post request and recieve a failure response
        response = self.client.post(register_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"}) 
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Last Name", str(response.data))

    def test_registration_when_missing_username(self):
        """
        fails to creates user due to missing username
        (Post Request)
        """

        self.data = {
            "first_name" : "Paul",
            "last_name" : "Pogba",
            "username" : "",
            "email" : "paulie_pogba@gmail.com",
            "password" : "password1234"
        }

        # make a post request and recieve a failure response
        response = self.client.post(register_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Username", str(response.data))

    def test_registration_when_missing_email(self):
        """
        fails to creates user due to missing email
        (Post Request)
        """

        self.data = {
            "first_name" : "Paul",
            "last_name" : "Pogba",
            "username" : "paulie_pogba",
            "email" : "",
            "password" : "password1234"
        }

        # make a post request and recieve a failure response
        response = self.client.post(register_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Email", str(response.data))

    def test_registration_when_missing_password(self):
        """
        fails to creates user due to missing password
        (Post Request)
        """

        self.data = {
            "first_name" : "Paul",
            "last_name" : "Pogba",
            "username" : "paulie_pogba",
            "email" : "paulie_pogba@gmail.com",
            "password" : ""
        }

        # make a post request and recieve a failure response
        response = self.client.post(register_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Missing Password", str(response.data))

    def test_registration_using_duplicate_username(self):
        """
        fails to create user due to duplicate username
        (Post Request)
        """
        # create initial user
        response = self.client.post(register_url, data=json.dumps(self.user_zero), headers={"Content-Type": "application/json"})

        # create new user with duplicate username
        self.data = {
            "first_name" : "Paul",
            "last_name" : "Pogba",
            "username" : "kungfukenny",
            "email" : "paulie_pogba@gmail.com",
            "password" : "password1234"
        }

        # make a post request and recieve a failure response
        response = self.client.post(register_url, data=json.dumps(self.data), headers={"Content-Type": "application/json"})
        self.assertEqual(response.status, "409 CONFLICT")
        self.assertIn("Error. Username Already Exists", str(response.data))


    def test_registration_using_duplicate_email(self):
        """
        fails to create user due to duplicate email
        (POST Request)
        """

        # create initial user
        response = self.client.post(register_url, data=json.dumps(self.user_zero), headers={"Content-Type":"application/json"})

        #create new user with duplicate email
        self.data = {
            "first_name" : "Paul",
            "last_name" : "Pogba",
            "username" : "paulie_pogba",
            "email" : "kdot@gmail.com",
            "password" : "password1234"
        }

        # make a post request and recieve a failure response
        response = self.client.post(register_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status, "409 CONFLICT")
        self.assertIn("Error. Email Address Already Exists", str(response.data))

    def test_registration_using_invalid_first_name(self):
        """
        fails to create user due to invalid first name format
        (POST Request)
        """

        self.data = {
            "first_name" : "jsd@76s",
            "last_name" : "walker",
            "username" : "kyliewalker",
            "email" : "kylie@gmail.com",
            "password" : "password1234"
        }

        # make a post request and recieve a failure response
        response = self.client.post(register_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. First Name Has Invalid Characters", str(response.data))

    def test_registration_using_invalid_last_name(self):
        """
        fails to create user due to invalid last name format
        (POST Request)
        """

        self.data = {
            "first_name" : "Kyle",
            "last_name" : "9sd9@",
            "username" : "kyliewalker",
            "email" : "kylie@gmail.com",
            "password" : "password1234"
        }

        # make a post request and recieve a failure response
        response = self.client.post(register_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Last Name Has Invalid Characters", str(response.data))

    def test_registration_using_invalid_username(self):
        """
        fails to create user due to invalid username format
        (POST Request)
        """

        self.data = {
            "first_name" : "Kyle",
            "last_name" : "Walker",
            "username" : "&c$6*C&HcbBj",
            "email" : "kylie@gmail.com",
            "password" : "password1234"
        }

        # make a post request and recieve a failure response
        response = self.client.post(register_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Username Has Invalid Characters", str(response.data))

    def test_registration_using_invalid_email(self):
        """
        fails to create user due to invalid email format
        (POST Request)
        """

        self.data = {
            "first_name" : "Kyle",
            "last_name" : "Walker",
            "username" : "kyliewalker",
            "email" : "kylie@gmail",
            "password" : "password1234"
        }

        # make a post request and recieve a failure response
        response = self.client.post(register_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Invalid Email Format", str(response.data))

    def test_succesfull_user_login(self):
        """
        succesfully logs in user to system
        (POST Request)
        """

        # create initial user
        response = self.client.post(register_url, data=json.dumps(self.user_zero), headers={"Content-Type":"application/json"})

        #log in using user credentials
        self.data = {
            "email" : "kdot@gmail.com",
            "password" : "password1234"
        }

         # make a post request and recieve a success response
        response = self.client.post(login_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        # self.assertEqual(response.status, 200)
        self.assertIn("You have succesfully logged in. Welcome", str(response.data))

    def test_user_login_with_missing_email(self):
        """
        fails to log in user with missing email
        (POST Request)
        """

        # create initial user
        response = self.client.post(register_url, data=json.dumps(self.user_zero), headers={"Content-Type":"application/json"})

        #log in using user credentials
        self.data = {
            "email" : "",
            "password" : "password1234"
        }

         # make a post request and recieve a Failure response
        response = self.client.post(login_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error: Missing Valid Email Address", str(response.data))

    def test_user_login_with_missing_password(self):
        """
        fails to log in user with missing password
        (POST Request)
        """

        # create initial user
        response = self.client.post(register_url, data=json.dumps(self.user_zero), headers={"Content-Type":"application/json"})

        #log in using user credentials
        self.data = {
            "email" : "kdot@gmail.com",
            "password" : ""
        }

         # make a post request and recieve a Failure response
        response = self.client.post(login_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error: Missing Password", str(response.data))


    def test_user_login_with_wrong_or_nonexisting_email(self):
        """
        fails to log in user with wrong email
        (POST Request)
        """

        # create initial user
        response = self.client.post(register_url, data=json.dumps(self.user_zero), headers={"Content-Type":"application/json"})

        #log in using user credentials
        self.data = {
            "email" : "kilodot@gmail.com",
            "password" : "password"
        }

         # make a post request and recieve a Failure response
        response = self.client.post(login_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error: Invalid Email or Password", str(response.data))

    def test_user_login_with_wrong_or_nonexisting_password(self):
        """
        fails to log in user with wrong password
        (POST Request)
        """

        # create initial user
        response = self.client.post(register_url, data=json.dumps(self.user_zero), headers={"Content-Type":"application/json"})

        #log in using user credentials
        self.data = {
            "email" : "kdot@gmail.com",
            "password" : "password"
        }

         # make a post request and recieve a Failure response
        response = self.client.post(login_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error: Invalid Email or Password", str(response.data))

    def test_user_login_with_invalid_email(self):
        """
        fails to log in user with invalid email format
        """
        # create initial user
        response = self.client.post(register_url, data=json.dumps(self.user_zero), headers={"Content-Type":"application/json"})

        #log in using user credentials
        self.data = {
            "email" : "kdot@gmail.",
            "password" : "password"
        }

         # make a post request and recieve a Failure response
        response = self.client.post(login_url, data=json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEqual(response.status, "400 BAD REQUEST")
        self.assertIn("Error. Invalid Email Format", str(response.data))
