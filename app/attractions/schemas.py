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

    @post_load
    def make_attraction(self, data, **kwargs):
        from .models import Attraction
        return Attraction(**data)

    def format_json_field(self, obj, field_name):
        field_value = getattr(obj, field_name)
        if not field_value:
            return []
            
        # 如果已经是列表格式，直接返回
        if isinstance(field_value, list):
            return field_value
            
        # 处理字符串类型的字段值
        if isinstance(field_value, str):
            try:
                # 尝试直接解析JSON
                parsed = json.loads(field_value)
                if isinstance(parsed, list):
                    return parsed
                return [parsed]
            except json.JSONDecodeError:
                # 处理特殊格式的字符串数组
                if field_name in ['features', 'images', 'tags', 'tips']:
                    # 处理被拆分的字符数组（如用户示例）
                    if any(c in field_value for c in ['["', '","', '"]']):
                        # 尝试提取所有引号内的内容
                        import re
                        # 先尝试直接组合所有字符
                        if all(len(c) == 1 for c in field_value if c not in ['[', ']', '"', ',']):
                            combined = ''.join(field_value)
                            try:
                                return json.loads(combined)
                            except:
                                pass
                        # 如果直接组合失败，再尝试提取引号内的内容
                        matches = re.findall(r'"([^"]*)"', field_value)
                        if matches:
                            return matches
                        
                    # 尝试清理并重新组合被拆分的JSON数组
                    cleaned = field_value.replace(' ', '').replace('\n', '')
                    if cleaned.startswith('["') and cleaned.endswith('"]'):
                        try:
                            return json.loads(cleaned)
                        except:
                            pass
                
                # 如果解析失败，返回包含原始值的数组
                return [field_value]
        
        # 其他情况返回包含原始值的数组
        return [field_value]

attraction_schema = AttractionSchema()
attractions_schema = AttractionSchema(many=True)