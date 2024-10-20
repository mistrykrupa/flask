from flask import Flask,render_template,redirect, url_for 
from views.auth_view import auth_bp
from views.purchase_view import purchase_bp
# from views.purchase_detail_view import purchase_details

from config import Config
from flask_jwt_extended import JWTManager, jwt_required

app = Flask(__name__,  static_folder='static')
app.config.from_object(Config)

jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(purchase_bp)

if __name__=='__main__':
    app.run(debug=True)

