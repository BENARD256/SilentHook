from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app=app) 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reward_name = db.Column(db.String(50), db.ForeignKey('user.id'))
    user_reward = db.relationship('User', backref='rewards')



if __name__ == '__main__':
    app.run(debug=True)
