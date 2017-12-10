import os
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS

# local import
from instance.config import app_config

db = MongoEngine()


def create_app(config_name):
    """
    creates instance of application
    :param config_name:
    :return:
    """
    app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.curdir), 'instance'), instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    from .auth import auth_blueprint
    from .store import store_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(store_blueprint)

    db.init_app(app)

    @app.route('/')
    def index():
        """
        index route for api
        :return: string
        """
        return "hello world"

    return app
