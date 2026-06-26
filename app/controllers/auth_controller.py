from flask import Blueprint, request, jsonify
from flask_babel import gettext as _
from flask_jwt_extended import create_access_token
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': _('Username and password required')}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': _('Username already exists')}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': _('User registered successfully')}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': _('Invalid username or password')}), 401
        
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token}), 200
