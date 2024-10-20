import json
import psycopg2
# from psycopg2.extras import RealDictCursor
# from flask import make_response
from config import  Config
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel:
    @staticmethod
    def get_db_connection():
        return psycopg2.connect(Config.DATABASE_URI)
    
    @staticmethod
    def create_user(username,password):
        password_hash = generate_password_hash(password)
        connection = UserModel.get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(username,password_hash) VALUES (%s,%s)",
                (username,password_hash)
            )
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            print(f"Error occurred: {str(e)}")# print(f"Error : {e}")
            return False
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_username(username):
        connection = UserModel.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s",(username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        return user
    
    @staticmethod
    def verify_password(stored_password_hash,provided_password):
        return check_password_hash(stored_password_hash, provided_password)