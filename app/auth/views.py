import re
from flask import Flask, Blueprint
from flask_restful import Resource, Api, reqparse
from . import auth_blueprint
from ..models import User

api_auth = Api(auth_blueprint)


class Registration(Resource):
    """
    Api resource for Registration of a user
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('first_name', required=True, help="Error. Missing First Name", location='json')
        self.parser.add_argument('last_name', required=True, help="Error. Missing Last Name", location='json')
        self.parser.add_argument('username', required=True, help="Error. Missing Username", location='json')
        self.parser.add_argument('email', required=True, help="Error. Missing Email", location='json')
        self.parser.add_argument('password', required=True, help="Error. Missing Password", location='json')
        
    def post(self):
        """
        Post request to Register user
        """
        args = self.parser.parse_args()

        # confirm first name value exists and is valid format
        firstname = args['first_name']
        if not firstname:
            response = {
                'message': 'Error. Missing First Name'
                }

            return response, 400
        check_firstname = re.match('^[a-zA-Z]+$', firstname)
        if check_firstname is None:
            response = {
                'message': 'Error. First Name Has Invalid Characters'
            }
            # return a response notifying the user that credentials username is invalid
            return response, 400

        # confirm last name value exists and is valid format
        lastname = args['last_name']
        if not lastname:
            response = {
                'message': 'Error. Missing Last Name'
            }

            return response, 400

        check_lastname = re.match('^[a-zA-Z]+$', lastname)
        if check_lastname is None:
            response = {
                'message': 'Error. Last Name Has Invalid Characters'
            }
            # return a response notifying the user that credentials username is invalid
            return (response, 400)

        # confirm username name value exists and is valid format
        username = args['username']
        if not username:
            response = {
                'message': 'Error. Missing Username'
            }

            return response, 400

        check_username = re.match('^[a-zA-Z0-9_.-]+$', username)
        if check_username is None:
            response = {
                'message': 'Error. Username Has Invalid Characters'
            }
            # return a response notifying the user that credentials username is invalid
            return response, 400

        # confirm email value exists and is valid format
        email = args['email']
        if not email:
            response = {
                'message': 'Error. Missing Email'
            }

            return response, 400
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

        if match is None:
            response = {
                'message': 'Error. Invalid Email Format'
            }
            
            return response, 400

        # confirm password value exists and is valid format
        password = args['password']
        if not password:
            response = {
                'message': 'Error. Missing Password'
            }

            return response, 400

        # Query to see if the username or email already exists
        username = User.query.filter_by(username=args["username"]).first()
        email = User.query.filter_by(email=args["email"]).first()

        if not username and not email:
            # this means there doesn't exist a user with the same username and email
            # proceed to register them
            try:
                user = User(
                    first_name=args['first_name'],
                    last_name=args['last_name'],
                    username=args['username'],
                    email=args['email'],
                    password=args['password'])

                user.save()

                response = {
                    'message': 'Success. You have registered. You can Log in'
                }

                return response, 201
            except Exception as e:
                # An error has occured, therefore return a string message containing the error
                response = {
                    'status': 'error',
                    'message': str(e)
                }
                return response, 500

        elif username:
            response = {
                'message': 'Error. Username Already Exists'
                }

            return response, 409

        else:
            response = {
                'message': 'Error. Email Address Already Exists'
                }

            return response, 409

  
class Login(Resource):
    """
    Api resource for logging in a user to the system
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', required=True, help="Error. Missing email", location='json')
        self.parser.add_argument('password', required=True, help="Error. Missing password", location='json')
    
    def post(self):
        """
        Post request to Register user
        """
        args = self.parser.parse_args()
        # confirm email value exists and is valid format
        email = args['email']
        if not email:
            response = {
                'message': 'Error: Missing Valid Email Address'
            }

            return response, 400
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

        if match is None:
            response = {
                'message': 'Error. Invalid Email Format'
            }
            
            return response, 400

        # confirm password value exists and is valid format
        password = args['password']
        if not password:
            response = {
                'message': 'Error: Missing Password'
            }

            return response, 400

        try:
            user = User.query.filter_by(email=args["email"]).first()

            if user and user.password_is_valid(password=args["password"]):
                access_token = user.generate_auth_token()
                if access_token:
                    response = {
                        'message': 'You have succesfully logged in. Welcome',
                        'access_token': access_token.decode()
                    }
                    return response, 200
            else:
                response = {
                    'message': 'Error: Invalid Email or Password'
                }
                return response, 400

        except Exception as e:
            response = {
                    'status': 'error',
                    'message': str(e)
                }
            return response, 500

# make resource accessible to the system
# http://127.0.0.1:5000/navyget-api/v1/auth/register
# http://127.0.0.1:5000/navyget-api/v1/auth/login


api_auth.add_resource(Registration, '/navyget-api/v1/auth/register')
api_auth.add_resource(Login, '/navyget-api/v1/auth/login')