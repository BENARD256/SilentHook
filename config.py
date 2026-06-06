import os
from urllib.parse import quote_plus # handles special Characters
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Read from env and encode safely
username = quote_plus(os.getenv("DB_USERNAME", "dbbd_admin"))
password = quote_plus(os.getenv("DB_PASSWORD", "admin@1234"))
database_name = quote_plus(os.getenv("DB_NAME", "dbbd"))
host = quote_plus(os.getenv("DB_HOST", "127.0.0.1"))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Config
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


    # CALLBACK_URL
    CALLBACK_URL = os.environ.get('CALLBACK_URL', 'http://127.0.0.1:5000')
    #CALLBACK_URL = "http://dbbd-61716.portmap.host:61716"
    #CALLBACK_URL = "http://192.168.100.10:5000"
    #CALLBACK_URL  = "http://5ae1-41-210-143-103.ngrok-free.app"

    # MSQL DECOY SERVER PORT
    MYSQL_PORT = 3308 # Required for running a Decoy Sql Server

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{username}:{password}@{host}:3306/{database_name}"

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{username}:{password}@{host}:3306/{database_name}"

