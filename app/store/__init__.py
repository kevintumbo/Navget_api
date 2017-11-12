# initialize blueprint
from flask import Blueprint

#This instance of a blueprint that represents the authentication blueprint

store_blueprint = Blueprint('store', __name__)

from . import views