#!flask/bin/python
import json

from flask import Response, g, Blueprint

from app.flaskrun import flaskrun

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)


if __name__ == '__main__':
    flaskrun(application)
