from config import Config, DevelopmentConfig, ProductionConfig
from models import baits, db

from flask import Flask, request, render_template, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
    
app.config.from_object(DevelopmentConfig) # Db Connection String
    
db.init_app(app) #initializing Db


@app.route("/", methods=['GET'])
def get_baits():
    baits = baits.query.get('id').fetchon()
    
   
    
    #return jsonify([bait.to_dict() for bait in baits]), 200
    return jsonify({'message':"Processing Baits"}), 200




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
    app.run(debug=True)

