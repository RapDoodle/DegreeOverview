# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies

from utils.hash import verify_hash
from core.exception import excpetion_handler

from models.user import User

VERSION = 'v1'
ENDPOINT = f'@RESTFUL_PREFIX::/{VERSION}/login'

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='The username of the user cannot be empty.'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='The password field cannot be empty.'
                        )

    @excpetion_handler
    def post(self):
        data = UserLogin.parser.parse_args()
        user = User.find_user_by_username(data['username'])
        if user is None:
            return {'message': 'User does not exists.'}, 400
        if not user.verify_password(data['password']):
            return {'message': 'Incorrect password.'}, 400
        response = jsonify({'message': 'Logged in successfully.'})
        access_token = create_access_token(identity=user.get_id())
        set_access_cookies(response, access_token)
        return response
