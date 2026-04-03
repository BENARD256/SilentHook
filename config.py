import os
from urllib.parse import quote_plus # handles special Characters
 
 # Ensuring Proper Encoding of Special Characters in Connection String
username = quote_plus("dbbd_admin")
password = quote_plus('admin@1234')
database_name = quote_plus("dbbd")
host = quote_plus("127.0.0.1")


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Config
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # Call_Back_Url
    CALL_BACK_URL = "http://127.0.0.1/callback.png"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{username}:{password}@{host}:3306/{database_name}"

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{username}:{password}@{host}:3306/{database_name}"

