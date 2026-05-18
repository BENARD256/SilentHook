from app.extensions import db
from datetime import datetime


class Mysql_events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), db.ForeignKey('triggers.token'), nullable=False)
    user = db.Column(db.String(50), nullable=False)
    hostname = db.Column(db.String(255), nullable=False)
    db_name = db.Column(db.String(50), nullable=False)
    source_ip = db.Column(db.String(50), nullable=False)
    event_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<mysql_events {self.id}>"