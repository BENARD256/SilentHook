#from config import Config, DevelopmentConfig, ProductionConfig
#from models import db # Database Module


## updated imports 
from .extensions import jwt, cache      # Import initialized extensions
from .extensions import db # Importing db from extensions
from .config import Config, DevelopmentConfig, ProductionConfig # Importing Configurations

#Blueprints
from .blueprints.auth import auth_bp, auth_api_bp # Auth Blueprint for APIs & Page Routes
from .blueprints.baits import baits_bp # Baits Blueprint
from .blueprints.triggers import triggers_bp # Triggers Blueprint
from .blueprints.alerts import callback_bp # Alerts (callback) Blueprint
from .blueprints import views # HTML Page Rendering


# blue prints
#from blueprints.auth import auth_bp, auth_api_bp # Auth Blueprint for APIs & Page Routes
#from blueprints.baits import baits_bp # Baits Blueprint
#from blueprints.triggers import triggers_bp # Triggers Blueprint
#from blueprints.alerts import callback_bp # Alerts (callback) Blueprint
#from blueprints import views # HTML Page Rendering 

##/
from flask import Flask, request, render_template, jsonify
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from datetime import timedelta

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config) # Load Configurations

    app.config.from_object({
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_HOST': 'redis',  # Redis container name or IP address
    'CACHE_REDIS_PORT': 6379,      # Redis default port
    'CACHE_REDIS_DB': 0,            # Redis database index
    'CACHE_DEFAULT_TIMEOUT': 300,     # Cache timeout in seconds (5 minutes)
    'JWT_TOKEN_LOCATION': ['cookies', 'headers'],
    'JWT_COOKIE_SECURE': False,
    'JWT_COOKIE_HTTPONLY': True,
    'JWT_COOKIE_SAMESITE': 'Lax',
    'JWT_ACCESS_TOKEN_EXPIRES': timedelta(hours=2),
    })

    db.init_app(app) # Initializing Db with app context
    jwt.init_app(app) # Initializing JWT Manager with app context
    cache.init_app(app) # Initializing Cache with app context

    with app.app_context():
        _register_blueprints(app) # Registering Blueprints
    return app

def _register_blueprints(app):
    app.url_map.strict_slashes = False
    
    
    from .blueprints.auth import auth_bp, auth_api_bp
    from .blueprints.baits import baits_bp
    from .blueprints.triggers import triggers_bp
    from .blueprints.alerts import callback_bp
    from .blueprints.views import views_bp, auth_page_bp 
    
    app.register_blueprint(auth_bp) # Registering Auth Blueprint
    app.register_blueprint(auth_api_bp) # Registering Auth API blueprint

    app.register_blueprint(baits_bp) # Registering Baits Blueprint
    app.register_blueprint(triggers_bp) # Registering Triggers Blueprint
    app.register_blueprint(callback_bp) # Registering Alerts Blueprint

    app.register_blueprint(views_bp) # Generale Blueprint for HTML Pages
    app.register_blueprint(auth_page_bp) # Blueprint for Auth Page Routes
def _test_db_connection(app): # Function to test DB connection
    try:
        with app.app_context():
            db.engine.connect()
    except Exception as e:
        print(f"Database Connection Failed: {e}")
    else:
        print("[+] Database Connection Successful [+]")



if __name__ == "__main__":
    app = create_app()
    _test_db_connection(app) # Testing DB Connection    
    _register_blueprints(app)

    app.run(debug=True, host='0.0.0.0')

