import pymongo
from flask import Flask, g

from app.main import main
from app.api.auth import auth
from app.config import config

application = Flask(__name__)
application.config.update(config)

application.register_blueprint(main)
application.register_blueprint(auth, url_prefix='/api/auth')

@application.teardown_appcontext
def close_db(error):
    if hasattr(g, 'client'):
        g.client.close()
