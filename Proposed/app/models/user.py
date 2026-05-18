from app.extensions import db, jwt, cache # Importing Extensions for DB, JWT, and Caching
from app.config import Config, DevelopmentConfig, ProductionConfig # Importing Configurations

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.id} - {self.username} - {self.email}>'