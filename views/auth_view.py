from flask import Blueprint,request,jsonify
from controller.auth_controller import AuthController

auth_bp = Blueprint('auth_bp',__name__)

@auth_bp.route('/register',methods=['POST'])
def register():
    data= request.get_json()
    result = AuthController.register_user(data)
    
    return result
    
@auth_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    result = AuthController.login_user(data)
    return result

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logged out successfully!'}), 200