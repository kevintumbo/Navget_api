from flask import Flask, Blueprint
from flask_restful import Resource, Api
from . import store_blueprint

api_store = Api(store_blueprint)
