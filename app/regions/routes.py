from flask import Blueprint, jsonify
from .models import Region
from app.attractions.models import Attraction
from app import db

regions_bp = Blueprint('regions', __name__)

@regions_bp.route('/regions', methods=['GET'])
def get_all_regions():
    regions = Region.query.all()
    return jsonify([region.to_dict() for region in regions]), 200

@regions_bp.route('/regions/<int:id>/attractions', methods=['GET'])
def get_attractions_by_region(id):
    region = Region.query.get_or_404(id)
    attractions = Attraction.query.filter_by(region_id=id).all()
    return jsonify([{
        'id': attraction.id,
        'name': attraction.name,
        'location': attraction.location,
        'rating': attraction.rating
    } for attraction in attractions]), 200