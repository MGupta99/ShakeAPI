#!flask/bin/python
import json

from flask import Flask, Response
import pymongo

from app.flaskrun import flaskrun
from app.api.auth import auth
from app.config import config

application = Flask(__name__)
application.register_blueprint(auth, url_prefix='/api/auth')
application.config.update(config)


client = pymongo.MongoClient(application.config['MONGO_CONNECTION'])
db = client.ShakeDev


@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)


if __name__ == '__main__':
    flaskrun(application)
