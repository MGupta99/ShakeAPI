import os
import base64
import time
import datetime
from datetime import timedelta
import requests

import jwt
from jwt import PyJWKClient, exceptions

from app.application import application

def validate_user(authRequest):
    if not validate_id_token(authRequest['identityToken']):
        return {}

    return verify

def validate_id_token(identity_token):
    identity_token = base64.b64decode(identity_token)
    jwk_client = PyJWKClient('https://appleid.apple.com/auth/keys')
    signing_key = jwk_client.get_signing_key_from_jwt(identity_token)

    try:
        data = jwt.decode(
            identity_token,
            signing_key.key,
            algorithms=['RS256'],
            audience=application.config['BUNDLE_ID'],
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
    headers = {
        'kid': application.config['SHAKE_KID'],
        'alg': 'ES256'
    }

    payload = {
        'iss': application.config['TEAM_ID'],
        'iat': time.time(),
        'exp': time.time() + timedelta(days=180).total_seconds(),
        'aud': 'https://appleid.apple.com',
        'sub': application.config['BUNDLE_ID']
    }

    private_key = open(os.path.expanduser(application.config['PRIVATE_KEY'])).read()

    client_secret = jwt.encode(
        payload,
        private_key,
        algorithm='ES256',
        headers=headers
    )

    resp = requests.post(
        'https://appleid.apple.com/auth/token',
        data={
            'client_id': application.config['BUNDLE_ID'],
            'client_secret': client_secret,
            'code': auth_code,
            'grant_type': 'authorization_code',
        },
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
    )

    if resp.status_code != 200:
        return {}

    resp_data = resp.json()

    print(resp_data['id_token'])
    return resp_data['refresh_token']
