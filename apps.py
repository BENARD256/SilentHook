from config import Config, DevelopmentConfig, ProductionConfig 
from models import db # Database Module

# blue prints
from blueprints.auth import auth_bp # Importing Auth Blueprint


from flask import Flask, request, render_template, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
    
app.config.from_object(DevelopmentConfig) # Db Connection String
    
db.init_app(app) #initializing Db


@app.route("/", methods=['GET'])
def index():
    return jsonify({"message":"Homepage"})

























def register_blueprints():
    app.register_blueprint(auth_bp) # Registering Auth Blueprint



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

