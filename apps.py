from config import Config, DevelopmentConfig, ProductionConfig
from models import db # Database Module
# blue prints
from blueprints.auth import auth_bp # Auth Blueprint
from blueprints.baits import baits_bp # Baits Blueprint
from blueprints.triggers import triggers_bp # Triggers Blueprint

from flask import Flask, request, render_template, jsonify
from flask_jwt_extended import JWTManager


app = Flask(__name__)

app.config.from_object(DevelopmentConfig) # DB Connection String

db.init_app(app) #initializing Db

jwt = JWTManager(app) # Initializing JWT Manager


@app.route("/", methods=['GET'])
def index():
    return jsonify({"message":"Homepage"})

























def register_blueprints():
    app.register_blueprint(auth_bp) # Registering Auth Blueprint
    app.register_blueprint(baits_bp) # Registering Baits Blueprint
    app.register_blueprint(triggers_bp) # Registering Triggers Blueprint


def test_db_connection(): # Function to test DB connection
    try:
        with app.app_context():
            db.engine.connect()
    except Exception as e:
        print(f"Database Connection Failed: {e}")
    else:
        print("[+] Database Connection Successful [+]")



if __name__ == "__main__":
    test_db_connection()
    register_blueprints()

    app.run(debug=True)

