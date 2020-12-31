import pymongo
from flask import Flask, g

from app.main import main
from app.api.auth import auth
from app.config import config

application = Flask(__name__)
application.config.update(config)

application.register_blueprint(main)
application.register_blueprint(auth, url_prefix='/api/auth')

@application.before_app_request
def get_db():
    g.client = pymongo.MongoClient(application.config['MONGO_CONNECTION'])
    g.db = g.client.ShakeDev

@application.after_app_request
def close_db():
    g.client.close()
