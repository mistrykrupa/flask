import os
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY','secretKey')
    DATABASE_URI = 'postgresql://krupa:123@localhost/flask_db'
    JWT_SECRET_KEY = 'secretKey' 