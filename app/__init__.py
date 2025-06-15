from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from config import Config

# 初始化数据库连接
db = SQLAlchemy()
# 初始化序列化工具
ma = Marshmallow()

# 应用工厂函数，创建Flask应用实例
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    ma.init_app(app)
    
    # 配置CORS - 统一配置所有路由
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": "*",
            "supports_credentials": True
        }
    })

    # 注册蓝图
    from app.auth import auth_bp
    from app.users import users_bp
    from app.attractions.routes import attractions_bp
    from app.reviews.routes import reviews_bp
    
    from app.topics.routes import topics_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(attractions_bp)
    app.register_blueprint(reviews_bp)
    
    app.register_blueprint(topics_bp)

    return app