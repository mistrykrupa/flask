import jwt
import datetime
from flask import jsonify
from flask import request
from model.user_model import UserModel
from services.auth_service import AuthService
from config import Config



class AuthController:

    @staticmethod
    def register_user(data):
        username = data.get('username')
        password = data.get('password')

        if UserModel.find_username(username):
            return jsonify({'message': 'Username already exists!'}), 400

        if UserModel.create_user(username,password):
            return jsonify({'message':'User registered successfully!'}),201
        else:
            return jsonify({'message':'Error registering user'}),500
        

    @staticmethod
    def login_user(data):
        username = data.get('username')
        password = data.get('password')


        result = AuthService.authenticate_user(username, password)
        return result