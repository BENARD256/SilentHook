# ALERT CALLBACKS
# All bait callbacks (FIM, Office files, domain) are handled here.
# Always validate the token before accessing any of its attributes. 

from app.extensions import db
from datetime import datetime

class Alerts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), db.ForeignKey('triggers.token'), nullable=False)
    source_ip = db.Column(db.String(50), nullable=False)
    user_agent = db.Column(db.String(255), nullable=False)
    event_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<alerts {self.id}>"
