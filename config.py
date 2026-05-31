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
    #JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "a9a807b1ab3c90e78dc6dda34bc38d9baa51cbcdcd281e24f8c0d13f62a7361b")


    # Call_Back_Url
    #CALLBACK_URL = os.environ.get('CALLBACK_URL', 'http://127.0.0.1:5000')
    #CALLBACK_URL  = "http://192.168.100.10:5000"
    #CALLBACK_URL = "http://dbbd-61716.portmap.host:61716"
    CALLBACK_URL = "http://192.168.100.10:5000"
    MYSQL_PORT = 3308 # Required for running a Decoy Sql Server

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{username}:{password}@{host}:3306/{database_name}"

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{username}:{password}@{host}:3306/{database_name}"

