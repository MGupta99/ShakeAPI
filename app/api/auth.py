import secrets

from flask import Blueprint, request, abort, jsonify, g

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

    user = request_body['user']
    api_key = secrets.token_hex(32)
    g.db.accounts.update_one(
        {'_id': user['id']},
        {
            'email': user['email'],
            'name': user['name'],
            'refresh_token': refresh_token,
            'api_key': api_key
        },
        upsert=True
    )

    return jsonify({'id': user['id'], 'api_key': api_key})


@auth.route('/apple/login', methods=['POST'])
def apple_login():
    request_body = request.get_json(silent=True)
    if request_body is None:
        return abort(400)

    refresh_token, error = validate_user(request_body)
    if error is not None:
        return abort(error)

    user_id = request_body['id']
    user = g.db.accounts.find_one({'_id': user_id}, projection=['api_key'])

    return jsonify(user) if user is not None else abort(404)
