from app import db

class Region(db.Model):
    __tablename__ = 'regions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50))  # 国内/国际
    parent_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    
    parent = db.relationship('Region', remote_side=[id], backref='sub_regions')
    attractions = db.relationship('Attraction', backref='region', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'parent_id': self.parent_id
        }