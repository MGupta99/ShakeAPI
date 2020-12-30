import pymongo
from flask import Flask, g

from app.api.auth import auth
from app.config import config

application = Flask(__name__)
application.config.update(config)
application.register_blueprint(auth, url_prefix='/api/auth')

client = pymongo.MongoClient(application.config['MONGO_CONNECTION'])
g.db = client.ShakeDev
