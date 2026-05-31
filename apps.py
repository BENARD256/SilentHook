from config import Config, DevelopmentConfig, ProductionConfig
from models import db # Database Module

# blue prints
from blueprints.auth import auth_bp, auth_api_bp # Auth Blueprint for APIs & Page Routes
from blueprints.baits import baits_bp # Baits Blueprint
from blueprints.triggers import triggers_bp # Triggers Blueprint
from blueprints.alerts import callback_bp, callback_domain_bp # Alerts (callback) Blueprint
from blueprints import views # HTML Page Rendering 
from blueprints.history import history_api_bp

from flask import Flask, request, render_template, jsonify
from flask_jwt_extended import JWTManager
from services.mysql.mysql_listener import start_mysql_listener # Starts Decoy Mysql Server for incoming alert
from flask import current_app

app = Flask(__name__)

app.config.from_object(DevelopmentConfig) # DB Connection String

db.init_app(app) #initializing Db

jwt = JWTManager(app) # Initializing JWT Manager


# Handle 404 Errors at app level
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def register_blueprints():
    app.url_map.strict_slashes = False
    app.register_blueprint(auth_bp) # Registering Auth Blueprint
    app.register_blueprint(auth_api_bp) # Registering Auth API blueprint

    app.register_blueprint(baits_bp) # Registering Baits Blueprint
    app.register_blueprint(triggers_bp) # Registering Triggers Blueprint
    app.register_blueprint(callback_bp) # Registering Alerts Blueprint
    app.register_blueprint(callback_domain_bp) # Registering DOMAIN callback Blueprint

    app.register_blueprint(views.views_bp) # Generale Blueprint for HTML Pages

    app.register_blueprint(history_api_bp) # Alert History
    

def test_db_connection(): # Function to test DB connection
    try:
        with app.app_context():
            db.engine.connect()
    except Exception as e:
        print(f"Database Connection Failed: {e}")
    else:
        print("[+] Database Connection Successful [+]")

register_blueprints() # Register Blueprints Ealier

if __name__ == "__main__":
    test_db_connection()
    start_mysql_listener(app, port=app.config['MYSQL_PORT']) # Starting Decoy Mysql Server
    app.run(debug=True, host='0.0.0.0', reloader_type='stat')
