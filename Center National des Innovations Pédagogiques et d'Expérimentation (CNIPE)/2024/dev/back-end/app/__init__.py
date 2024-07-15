from flask import Flask

from flask_pymongo import PyMongo
from config import Config
from flask_cors import CORS

mongo = PyMongo()

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    mongo.init_app(app)

    from app import routes
  
    app.register_blueprint(routes.bp)

    return app