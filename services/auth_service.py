import jwt
import datetime
from werkzeug.security import check_password_hash
from config import Config
from model.user_model import UserModel
from flask import jsonify

class AuthService:

    @staticmethod
    def generate_token(user_id):
        """Generates a JWT token for the user."""
        token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }, Config.SECRET_KEY, algorithm='HS256')
        
        return token

    @staticmethod
    def verify_password(stored_password_hash, provided_password):
        """Verifies that the stored hash matches the provided password."""
        return check_password_hash(stored_password_hash, provided_password)

    @staticmethod
    def authenticate_user(username, password):
        """Handles user authentication."""
        user = UserModel.find_by_username(username)
        if not user:
            return jsonify({'message':'Invalid username','error':True})
        
        passcheck = AuthService.verify_password(user[2], password)
        if passcheck:
                 token = jwt.encode({
                'user_id': username,
                'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60)},Config.SECRET_KEY,algorithm='HS256')
                 return jsonify({'token':token}),200
        else:
            return "Invalid credentials!"
