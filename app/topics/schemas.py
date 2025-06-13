from marshmallow import Schema, fields

class TopicSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    image = fields.Str()

topic_schema = TopicSchema()
topics_schema = TopicSchema(many=True)