from app.extensions import db
from datetime import datetime
from enum import Enum
from app.models.alert import Alerts
from app.models.mysql_events import Mysql_events
from app.models.watcher_events import Watcher_events


class Alert_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), db.ForeignKey('triggers.token'), nullable=False)
    recipient_addr = db.Column(db.String(50), nullable=False)
    delivery_status = db.Column(db.Enum('sent', 'failed'), default='sent')

    def __repr__(self):
        return f"<alert_history {self.id}>"