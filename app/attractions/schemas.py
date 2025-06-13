from marshmallow import Schema, fields, post_load
import json

class AttractionSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    location = fields.Str()
    description = fields.Str()
    history = fields.Str()
    features = fields.List(fields.Str())
    tips = fields.List(fields.Str())
    openTime = fields.Str()
    price = fields.Decimal()
    discountPrice = fields.Decimal()
    suggestedDuration = fields.Str()
    rating = fields.Float()
    reviewCount = fields.Int()
    tags = fields.List(fields.Str())
    images = fields.List(fields.Str())
    phone = fields.Str()
    website = fields.Str()

    def get_json_field(self, obj, field_name):
        field_value = getattr(obj, field_name)
        if isinstance(field_value, str):
            try:
                # 处理可能被拆分的JSON字符串
                if field_value.startswith('[') and field_value.endswith(']'):
                    # 如果是标准JSON数组格式，直接解析
                    return json.loads(field_value)
                else:
                    # 处理被拆分的字符数组
                    if field_name in ['features', 'tags', 'images', 'tips']:
                        # 尝试重新组合被拆分的JSON数组
                        try:
                            # 先去除所有空格和换行
                            cleaned = field_value.replace(' ', '').replace('\n', '')
                            # 如果是被拆分的JSON数组（如用户示例）
                            if '"' in cleaned or '[' in cleaned or ']' in cleaned:
                                # 直接解析整个字符串
                                return json.loads(cleaned)
                            else:
                                # 否则返回原始字符串
                                return [field_value]
                        except json.JSONDecodeError:
                            # 如果解析失败，返回原始字符串
                            return [field_value]
                    else:
                        return [field_value]
            except json.JSONDecodeError:
                return []
        return field_value

attraction_schema = AttractionSchema()
attractions_schema = AttractionSchema(many=True)