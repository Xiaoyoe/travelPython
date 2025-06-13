from app import db
import json

class Attraction(db.Model):
    __tablename__ = 'attractions'
    
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    description = db.Column(db.Text)
    history = db.Column(db.Text)
    features = db.Column(db.Text)
    tips = db.Column(db.Text)
    openTime = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 2))
    discountPrice = db.Column(db.Numeric(10, 2))
    suggestedDuration = db.Column(db.String(255))
    rating = db.Column(db.Float)
    reviewCount = db.Column(db.Integer)
    tags = db.Column(db.Text)
    images = db.Column(db.Text)
    phone = db.Column(db.String(255))
    website = db.Column(db.String(255))
    
    reviews = db.relationship('Review', backref='attraction', lazy=True)
    favorites = db.relationship('Favorite', backref='attraction', lazy=True)
    
    def get_features(self):
        return json.loads(self.features) if self.features else []
    
    def get_tips(self):
        return json.loads(self.tips) if self.tips else []
    
    def get_tags(self):
        return json.loads(self.tags) if self.tags else []
    
    def get_images(self):
        return json.loads(self.images) if self.images else []