#!flask/bin/python
import json

from flask import Response

from app.flaskrun import flaskrun
from app import application


@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)


if __name__ == '__main__':
    flaskrun(application)
