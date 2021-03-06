import os
import sys
import base64
import time
import datetime
from datetime import timedelta
import requests

import jwt
from jwt import PyJWKClient, exceptions
from flask import g
import pymongo

def validate_user(authRequest):
    id_token = authRequest.get('identityToken')

    if not validate_id_token(id_token):
        print('invalid identityToken', file=sys.stderr)
        return {}, 401

    auth_code = authRequest.get('authorizationCode')

    return verify_auth_code(authRequest['authorizationCode'])

def validate_id_token(identity_token):
    identity_token = base64.b64decode(identity_token)
    jwk_client = PyJWKClient('https://appleid.apple.com/auth/keys')
    signing_key = jwk_client.get_signing_key_from_jwt(identity_token)

    try:
        data = jwt.decode(
            identity_token,
            signing_key.key,
            algorithms=['RS256'],
            audience=os.environ['BUNDLE_ID'],
            issuer='https://appleid.apple.com',
            options={
                'verify_aud': True,
                'verify_exp': True,
                'verify_iss': True
            }
        )
    except exceptions.InvalidTokenError as error:
        return False

    return True

def verify_auth_code(auth_code):
    auth_code = base64.b64decode(auth_code)
    headers = {
        'kid': os.environ['SHAKE_KID'],
        'alg': 'ES256'
    }

    payload = {
        'iss': os.environ['TEAM_ID'],
        'iat': time.time(),
        'exp': time.time() + timedelta(days=180).total_seconds(),
        'aud': 'https://appleid.apple.com',
        'sub': os.environ['BUNDLE_ID']
    }

    private_key = open(os.path.expanduser(os.environ['PRIVATE_KEY'])).read()

    client_secret = jwt.encode(
        payload,
        private_key,
        algorithm='ES256',
        headers=headers
    )

    resp = requests.post(
        'https://appleid.apple.com/auth/token',
        data={
            'client_id': os.environ['BUNDLE_ID'],
            'client_secret': client_secret,
            'code': auth_code,
            'grant_type': 'authorization_code',
        },
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
    )

    if resp.status_code != 200:
        print('Unable to verify authorizationCode', file=sys.stderr)
        return {}, 403

    resp_data = resp.json()
    return resp_data['refresh_token'], None

def get_db():
    g.client = pymongo.MongoClient(os.environ['MONGO_CONNECTION'])
    g.db = g.client.ShakeDev
