from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<user {self.id}>"
    

class Baits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abbrev = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    bait_path = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<bait {self.id}>"

class Triggers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), nullable=False,unique=True) # has to be unique
    reminder = db.Column(db.String(255), nullable=False)
    callback_email = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # foregin key to users table
    bait_id = db.Column(db.Integer, db.ForeignKey('baits.id')) # foregin key to baits table 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationships for backward access (Join)
    bait = db.relationship('Baits', backref='triggers', lazy=True) # allows to fetch Bait Abbrev for emailing purposes (Which bait triggred alert)
    
    def __repr__(self):
        return f"<trigger {self.id}>"
    

class Alerts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), db.ForeignKey('triggers.token'), nullable=False) # token id to identify the trigger
    source_ip = db.Column(db.String(50), nullable=False)
    user_agent = db.Column(db.String(255), nullable=False)
    event_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<alerts {self.id}>"
    

class Watcher_events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), db.ForeignKey('triggers.token'), nullable=False)
    user = db.Column(db.String(50), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    access = db.Column(db.String(50), nullable=False)
    process = db.Column(db.String(255), nullable=False)
    source_ip = db.Column(db.String(50), nullable=False)
    event_time = db.Column(db.DateTime, default=datetime.utcnow)
    trigger_info = db.relationship("Triggers", backref='Watcher_events', lazy=True)
    
    def __repr__(self):
        return f"<watcher_event {self.id}>"
    

class Mysql_events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), db.ForeignKey('triggers.token'), nullable=False)
    user = db.Column(db.String(50), nullable=False)
    hostname = db.Column(db.String(255), nullable=False)
    db_name = db.Column(db.String(50), nullable=False)
    source_ip = db.Column(db.String(50), nullable=False)
    event_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<mysql_event {self.id}>"
    

class Alert_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), db.ForeignKey('triggers.token'), nullable=False)
    recipient_addr = db.Column(db.String(50), nullable=False)
    delivery_status = db.Column(db.Enum('sent', 'failed'), default='sent')

    def __repr__(self):
        return f"<alert_history {self.id}>"
    