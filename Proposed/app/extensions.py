from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
#from flask_migrate import Migrate

## global intialization of extensions to avoid circular imports and to be used across the application
db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
#migrate = Migrate() ## Initialize Flask-Migrate for handling database migrations