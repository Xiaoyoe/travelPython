from flask import Blueprint, request, jsonify
from app.attractions.models import Attraction
from app.categories.models import Category
from app.regions.models import Region
from app import db

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search_all():
    query = request.args.get('q')
    category_id = request.args.get('category')
    region_id = request.args.get('region')
    
    results = {
        'attractions': [],
        'categories': [],
        'regions': []
    }
    
    # 搜索景点
    if query:
        attractions = Attraction.query.filter(
            (Attraction.name.ilike(f'%{query}%')) |
            (Attraction.description.ilike(f'%{query}%'))
        )
        
        if category_id:
            attractions = attractions.filter_by(category_id=category_id)
        if region_id:
            attractions = attractions.filter_by(region_id=region_id)
        
        results['attractions'] = [{
            'id': a.id,
            'name': a.name,
            'description': a.description[:100] + '...' if a.description else '',
            'category_id': a.category_id,
            'region_id': a.region_id
        } for a in attractions.limit(10).all()]
    
    # 搜索分类
    if query and not category_id:
        categories = Category.query.filter(
            (Category.name.ilike(f'%{query}%')) |
            (Category.description.ilike(f'%{query}%'))
        ).limit(5).all()
        results['categories'] = [{
            'id': c.id,
            'name': c.name,
            'description': c.description[:100] + '...' if c.description else ''
        } for c in categories]
    
    # 搜索地区
    if query and not region_id:
        regions = Region.query.filter(
            Region.name.ilike(f'%{query}%')
        ).limit(5).all()
        results['regions'] = [{
            'id': r.id,
            'name': r.name,
            'type': r.type
        } for r in regions]
    
    return jsonify(results), 200