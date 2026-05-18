from app.extensions import db

class Baits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abbrev = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    bait_path = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<baits {self.id}>"