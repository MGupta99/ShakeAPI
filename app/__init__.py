import pymongo
from flask import Flask, g

from app.api.auth import auth
from app.config import config

application = Flask(__name__)
application.config.update(config)

with application.app_context():
    application.register_blueprint(auth, url_prefix='/api/auth')

client = pymongo.MongoClient(application.config['MONGO_CONNECTION'])
g.db = client.ShakeDev
