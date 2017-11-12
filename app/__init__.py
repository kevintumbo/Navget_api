import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.curdir), 'instance'), instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .auth import auth_blueprint
    from .store import store_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(store_blueprint)

    db.init_app(app)

    @app.route('/')
    def index():
        return "hello world"

    return app