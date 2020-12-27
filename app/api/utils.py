import requests

import jwt
from jwt import PyJWKClient

def verify_apple_token(identity_token, auth_code):
    jwk_client = PyJWKClient('https://appleid.apple.com/auth/keys')
    signing_key = jwk_client.get_signing_key_from_jwt(identity_token)

    data = jwt.decode(
        identity_token,
        signing_key.key,
        algorithms=['ES256'],
        audience='com.milangupta.Shake'
    )

    if data['iss'] != 'https://appleid.apple.com':
        return False

    
