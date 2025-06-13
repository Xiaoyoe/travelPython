from flask import Blueprint, request, jsonify
from app.reviews.models import Review
from app.reviews.schemas import review_schema, reviews_schema
from app import db

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/reviews', methods=['GET'])
def get_reviews():
    attraction_id = request.args.get('attractionId')
    if attraction_id:
        reviews = Review.query.filter_by(attractionId=attraction_id).all()
    else:
        reviews = Review.query.all()
    return jsonify(reviews_schema.dump(reviews))

@reviews_bp.route('/reviews/<int:id>', methods=['GET'])
def get_review(id):
    review = Review.query.get_or_404(id)
    return jsonify(review_schema.dump(review))

@reviews_bp.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    review = Review(**data)
    db.session.add(review)
    db.session.commit()
    return jsonify(review_schema.dump(review)), 201

@reviews_bp.route('/reviews/<int:id>', methods=['PUT'])
def update_review(id):
    review = Review.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(review, key, value)
    db.session.commit()
    return jsonify(review_schema.dump(review))

@reviews_bp.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return '', 204