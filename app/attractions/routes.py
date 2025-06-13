from flask import Blueprint, request, jsonify
from app.attractions.models import Attraction
from app.attractions.schemas import attraction_schema, attractions_schema
from app import db

attractions_bp = Blueprint('attractions', __name__)

@attractions_bp.route('/attractions', methods=['GET'])
def get_attractions():
    attractions = Attraction.query.all()
    return jsonify(attractions_schema.dump(attractions))

@attractions_bp.route('/attractions/<string:id>', methods=['GET'])
def get_attraction(id):
    attraction = Attraction.query.get_or_404(id)
    return jsonify(attraction_schema.dump(attraction))

@attractions_bp.route('/attractions', methods=['POST'])
def create_attraction():
    data = request.get_json()
    attraction = Attraction(**data)
    db.session.add(attraction)
    db.session.commit()
    return jsonify(attraction_schema.dump(attraction)), 201

@attractions_bp.route('/attractions/<string:id>', methods=['PUT'])
def update_attraction(id):
    attraction = Attraction.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(attraction, key, value)
    db.session.commit()
    return jsonify(attraction_schema.dump(attraction))

@attractions_bp.route('/attractions/<string:id>', methods=['DELETE'])
def delete_attraction(id):
    attraction = Attraction.query.get_or_404(id)
    db.session.delete(attraction)
    db.session.commit()
    return '', 204