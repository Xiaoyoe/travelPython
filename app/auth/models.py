from app import db
import json

# 用户模型，对应数据库中的users表
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    frequentCity = db.Column(db.String(255))
    preferences = db.Column(db.Text)
    
    reviews = db.relationship('Review', backref='user', lazy=True)

    
    def get_preferences(self):
        return json.loads(self.preferences) if self.preferences else []
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'email': self.email,
            'frequentCity': self.frequentCity,
            'preferences': self.get_preferences()
        }