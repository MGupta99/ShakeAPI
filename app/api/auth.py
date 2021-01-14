import sys
import os
import json
import uuid
import base64
import secrets
import datetime

from datetime import timedelta

import bcrypt
from flask import Blueprint, request, abort, jsonify, g
from flask_expects_json import expects_json
from twilio.rest import Client

from app.api.utils import validate_user, get_db
from app.schema import schema

auth = Blueprint('auth', __name__)
auth.before_request(get_db)

@auth.route('/apple/register', methods=['POST'])
@expects_json(schema['/apple/register'])
def apple_register():
    request_body = request.get_json()
    refresh_token, error = validate_user(request_body)
    if error is not None:
        return abort(error)

    user = request_body['user']
    api_key = secrets.token_hex(32)
    g.db.Accounts.update_one(
        {'_id': user['id']},
        {'$set': {
            'name': user['name'],
            'refresh_token': refresh_token,
            'api_key': api_key
        }},
        upsert=True
    )

    return jsonify({'_id': user['id'], 'api_key': api_key})


@auth.route('/apple/login', methods=['POST'])
@expects_json(schema['/apple/login'])
def apple_login():
    request_body = request.get_json()

    refresh_token, error = validate_user(request_body)
    if error is not None:
        return abort(error)

    user_id = request_body['id']
    user = g.db.Accounts.find_one({'_id': user_id}, projection=['api_key'])

    return jsonify(user) if user is not None else abort(404)


@auth.route('/password/otp/send', methods=['POST'])
@expects_json(schema['/password/otp/send'])
def send_otp():
    request_body = request.get_json()

    client = Client(os.environ['TWILIO_SID'], os.environ['TWILIO_AUTH_TOKEN'])

    otp = str(secrets.randbelow(1000000)).zfill(6)
    message = client.messages.create(
        body=f'Your Shake code is {otp}',
        from_='+18589433121',
        to=request_body['phoneNumber']
    )

    g.db.OTP.update_one(
        {'phone_number': request_body['phoneNumber']},
        {'$set': {
            'code': otp,
            'expires': datetime.datetime.utcnow() + timedelta(minutes=5),
        }},
        upsert=True
    )

    return jsonify({}), 200

@auth.route('/password/register', methods=['POST'])
@expects_json(schema['/password/register'])
def password_register():
    request_body = request.get_json()

    if g.db.Accounts.find_one({'phone_number': request_body['phoneNumber']}) is not None:
        return jsonify({'error_code': 'AlreadyExists'}), 409

    otp = g.db.OTP.find_one({
        'phone_number': request_body['phoneNumber'],
    })

    if datetime.datetime.utcnow() > otp['expires']:
        return jsonify({"error_code": "OTPExpired"}), 401

    if otp['code'] != request_body['code']:
        return jsonify({"error_code": "OTPInvalid"}), 401

    id = uuid.uuid4()
    api_key = secrets.token_hex(32)
    g.db.Accounts.insert_one({
        '_id': id,
        'api_key': api_key,
        'phone_number': request_body['phoneNumber'],
        'name': request_body['name'],
        'password': bcrypt.hashpw(request_body['password'].encode(), bcrypt.gensalt()),
    })

    return jsonify({'_id': id, 'api_key': api_key})

@auth.route('/password/login', methods=['POST'])
@expects_json(schema['/password/login'])
def password_login():
    request_body = request.get_json()

    user = g.db.Accounts.find_one({'phone_number': request_body['phone']}, projection=['password', 'api_key'])
    if not bcrypt.checkpw(request_body['password'].encode(), user['password']):
        return abort(401)

    return jsonify({'_id': user['_id'], 'api_key': user['api_key']})
