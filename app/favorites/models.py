from app import db

class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    attractionId = db.Column(db.String(255), db.ForeignKey('attractions.id'), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('userId', 'attractionId', name='_user_attraction_uc'),
    )