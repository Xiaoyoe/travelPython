from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from app import db
from app.auth.models import User
from .schemas import user_profile_schema
from app.auth.schemas import users_schema
import os
from werkzeug.utils import secure_filename

# 创建测试蓝图，使用唯一的名称
users_bp = Blueprint('users', __name__)


# 获取当前用户的个人资料   http://localhost:5000/users/profile?user_id=<用户ID>

@users_bp.route('/avatar', methods=['POST'])
def upload_avatar():
    if 'file' not in request.files:
        raise BadRequest('No file part')
    
    file = request.files['file']
    if file.filename == '':
        raise BadRequest('No selected file')
    
    if file:
        filename = secure_filename(file.filename)
        # 这里应该实现文件保存逻辑，实际项目中需要配置上传目录
        # file.save(os.path.join(upload_folder, filename))
        
        user_id = request.form.get('user_id')
        if not user_id:
            raise BadRequest('Missing user ID')
        
        user = User.query.get_or_404(user_id)
        user.avatar = filename  # 实际项目中应该保存文件路径或URL
        db.session.commit()
        
        return jsonify({'avatar': filename}), 200
@users_bp.route('/profile', methods=['GET'])
def get_user_profile():
    user_id = request.args.get('user_id')
    if not user_id:
        raise BadRequest('Missing user ID')
    user = User.query.get_or_404(user_id)  # 查询用户
    return jsonify(user_profile_schema.dump(user)), 200  # 返回用户资料


# 更新当前用户的个人资料
@users_bp.route('/profile', methods=['PUT'])
def update_user_profile():
    data = request.get_json()  # 获取JSON格式的请求数据

    if not data:
        raise BadRequest('No input data provided')

    user_id = request.args.get('user_id')
    if not user_id:
        raise BadRequest('Missing user ID')
    user = User.query.get_or_404(user_id)  # 查询用户

    # 更新用户资料（只更新请求中提供的字段）
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'phone' in data:
        user.phone = data['phone']
    if 'address' in data:
        user.address = data['address']

    db.session.commit()  # 提交数据库变更
    return jsonify(user_profile_schema.dump(user)), 200  # 返回更新后的用户资料


# 获取所有用户列表
@users_bp.route('/all', methods=['GET'])
def get_all_users():
    users = User.query.all()  # 查询所有用户
    return jsonify(users_schema.dump(users)), 200

@users_bp.route('/stats', methods=['GET'])
def get_user_stats():
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    # 获取用户总数
    total_users = db.session.query(func.count(User.id)).scalar()
    
    # 获取最近7天活跃用户数
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    active_users = db.session.query(func.count(User.id)).\
        filter(User.lastLogin >= seven_days_ago).scalar()
    
    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'active_percentage': round((active_users / total_users * 100) if total_users > 0 else 0, 2)
    }), 200  # 返回用户列表