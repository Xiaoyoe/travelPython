from flask import Blueprint, request, jsonify
from app.favorites.models import Favorite
from app.favorites.schemas import favorite_schema, favorites_schema
from app import db

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/favorites', methods=['GET'])
def get_favorites():
    user_id = request.args.get('userId')
    if user_id:
        favorites = Favorite.query.filter_by(userId=user_id).all()
    else:
        favorites = Favorite.query.all()
    return jsonify(favorites_schema.dump(favorites))

@favorites_bp.route('/favorites', methods=['POST'])
def create_favorite():
    data = request.get_json()
    favorite = Favorite(**data)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite_schema.dump(favorite)), 201

@favorites_bp.route('/favorites/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    favorite = Favorite.query.get_or_404(id)
    db.session.delete(favorite)
    db.session.commit()
    return '', 204