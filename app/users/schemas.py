from marshmallow import fields
from app import ma
import json

# 用户资料序列化
class UserProfileSchema(ma.Schema):
    id = fields.Integer()
    username = fields.String()
    nickname = fields.String()
    email = fields.String()
    frequentCity = fields.String()
    preferences = fields.Method('get_preferences')
    
    def get_preferences(self, obj):
        if isinstance(obj.preferences, str):
            try:
                return json.loads(obj.preferences)
            except json.JSONDecodeError:
                return []
        return obj.preferences

    class Meta:
        fields = ('id', 'username', 'nickname', 'email', 'frequentCity', 'preferences')

# 创建用户资料序列化器实例
user_profile_schema = UserProfileSchema()