from app.extensions import db
from datetime import datetime

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
        return f"<watcher_events {self.id}>"