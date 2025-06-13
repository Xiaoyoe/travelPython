from flask import Blueprint, request, jsonify
from app.topics.models import Topic
from app.topics.schemas import topic_schema, topics_schema
from app import db

topics_bp = Blueprint('topics', __name__)

@topics_bp.route('/topics', methods=['GET'])
def get_topics():
    topics = Topic.query.all()
    return jsonify(topics_schema.dump(topics))

@topics_bp.route('/topics/<int:id>', methods=['GET'])
def get_topic(id):
    topic = Topic.query.get_or_404(id)
    return jsonify(topic_schema.dump(topic))

@topics_bp.route('/topics', methods=['POST'])
def create_topic():
    data = request.get_json()
    topic = Topic(**data)
    db.session.add(topic)
    db.session.commit()
    return jsonify(topic_schema.dump(topic)), 201

@topics_bp.route('/topics/<int:id>', methods=['PUT'])
def update_topic(id):
    topic = Topic.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(topic, key, value)
    db.session.commit()
    return jsonify(topic_schema.dump(topic))

@topics_bp.route('/topics/<int:id>', methods=['DELETE'])
def delete_topic(id):
    topic = Topic.query.get_or_404(id)
    db.session.delete(topic)
    db.session.commit()
    return '', 204