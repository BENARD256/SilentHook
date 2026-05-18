from app.extensions import db
from datetime import datetime

class Triggers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), nullable=False, unique=True)
    reminder = db.Column(db.String(255), nullable=False)
    callback_email = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bait_id = db.Column(db.Integer, db.ForeignKey('baits.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bait = db.relationship('Baits', backref='triggers', lazy=True)

    def __repr__(self):
        return f"<trigger {self.id}>"