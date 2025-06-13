from marshmallow import fields
from app import ma
import json

# 用户数据序列化
class UserSchema(ma.Schema):
    id = fields.Integer()
    username = fields.String()
    password = fields.String(load_only=True)
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
        fields = ('id', 'username', 'password', 'nickname', 'email', 'frequentCity', 'preferences')

# 创建单用户和多用户的序列化器实例
user_schema = UserSchema()  # 用于单个用户
users_schema = UserSchema(many=True)  # 用于用户列表