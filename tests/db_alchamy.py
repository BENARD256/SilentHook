from flask import Flask, render_template, request, jsonify

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db' # Path to where the database file is located

#Initialising the Database

db = SQLAlchemy(app) #initialisation


# Creating a db model as a class
# its later auto translated into SQL queries

class Users(db.Model): # Creates table Users

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False) # Name can't be null
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	 
	# A functi:on to return a string when something is added
	def __repr__(self):
		return '<Name %r>' % self.id
		
	
subscribers = [] 