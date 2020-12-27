from flask import Blueprint, request

from app.api.utils import verify_apple_token

auth = Blueprint('auth', __name__)

@auth.route('/apple/register', methods=['POST'])
def apple_register():
    return 'Hello'

@auth.route('/apple/login', methods=['POST'])
def apple_login():
    return 'Hello'
