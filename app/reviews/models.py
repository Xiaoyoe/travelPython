from app import db
import json
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    attractionId = db.Column(db.String(255), db.ForeignKey('attractions.id'))
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    userName = db.Column(db.String(255))
    userAvatar = db.Column(db.String(255))
    rating = db.Column(db.Integer)
    content = db.Column(db.Text)
    images = db.Column(db.JSON)
    date = db.Column(db.Date, default=datetime.utcnow)
    
    def get_images(self):
        return self.images if self.images else []