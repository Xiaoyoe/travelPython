from app import db
import json

class Attraction(db.Model):
    __tablename__ = 'attractions'
    
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    description = db.Column(db.Text)
    history = db.Column(db.Text)
    features = db.Column(db.JSON)
    tips = db.Column(db.JSON)
    openTime = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 2))
    discountPrice = db.Column(db.Numeric(10, 2))
    suggestedDuration = db.Column(db.String(255))
    rating = db.Column(db.Float)
    reviewCount = db.Column(db.Integer)
    tags = db.Column(db.JSON)
    images = db.Column(db.JSON)
    phone = db.Column(db.String(255))
    website = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in ['features', 'tips', 'tags', 'images'] and isinstance(value, list):
                setattr(self, key, json.dumps(value, ensure_ascii=False))
            else:
                setattr(self, key, value)
    
    def get_features(self):
        return self._parse_json_field('features')
    
    def get_tips(self):
        return self._parse_json_field('tips')
    
    def get_tags(self):
        return self._parse_json_field('tags')
    
    def get_images(self):
        return self._parse_json_field('images')
    
    def _parse_json_field(self, field_name):
        field_value = getattr(self, field_name)
        if not field_value:
            return []
        if isinstance(field_value, list):
            return field_value
        if isinstance(field_value, str):
            try:
                return json.loads(field_value)
            except json.JSONDecodeError:
                return [field_value]
        return field_value