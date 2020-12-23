from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/apple/register')
def apple_register():
    return 'Hello'
