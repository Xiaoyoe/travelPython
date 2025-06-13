from marshmallow import Schema, fields

class FavoriteSchema(Schema):
    id = fields.Int()
    userId = fields.Int(required=True)
    attractionId = fields.Str(required=True)

favorite_schema = FavoriteSchema()
favorites_schema = FavoriteSchema(many=True)