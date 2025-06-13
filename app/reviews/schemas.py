from marshmallow import Schema, fields
from datetime import datetime

class ReviewSchema(Schema):
    id = fields.Int()
    attractionId = fields.Str(required=True)
    userId = fields.Int(required=True)
    userName = fields.Str()
    userAvatar = fields.Str()
    rating = fields.Int(required=True)
    content = fields.Str()
    images = fields.List(fields.Str())
    date = fields.Date()

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)