from flask import Blueprint, request, abort

from app.api.utils import validate_user

auth = Blueprint('auth', __name__)

@auth.route('/apple/register', methods=['POST'])
def apple_register():
    request_body = request.get_json(silent=True)
    if request_body is None:
        return abort(400)

    refresh_token, error = validate_user(request_body)
    if error is not None:
        return abort(error)

    

@auth.route('/apple/login', methods=['POST'])
def apple_login():
    print(request.get_json())
    return 'Hello'
