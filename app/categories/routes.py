from flask import Blueprint, jsonify
from .models import Category
from app.attractions.models import Attraction
from app import db

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET'])
def get_all_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories]), 200

@categories_bp.route('/categories/<int:id>/attractions', methods=['GET'])
def get_attractions_by_category(id):
    category = Category.query.get_or_404(id)
    attractions = Attraction.query.filter_by(category_id=id).all()
    return jsonify([{
        'id': attraction.id,
        'name': attraction.name,
        'location': attraction.location,
        'rating': attraction.rating
    } for attraction in attractions]), 200