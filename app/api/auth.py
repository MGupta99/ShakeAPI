from flask import Blueprint, request, abort

from app.api.utils import validate_user

auth = Blueprint('auth', __name__)

@auth.route('/apple/register', methods=['POST'])
def apple_register():
    if not verify_apple_token(request.get_json()):
        abort(401)

    return 'Hello'

@auth.route('/apple/login', methods=['POST'])
def apple_login():
    print(request.get_json())
    return 'Hello'
