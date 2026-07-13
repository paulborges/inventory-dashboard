from flask import request, jsonify
from app.routes import auth_bp
from app.database import db
from app.models import User
from app.auth import generate_token
from app.auth import token_required
from app.auth import admin_required

@auth_bp.route('/register', methods = ['POST'])
def register():
    """REGISTER NEW USER""" 
    try:
        data=request.get_json()

        if not data or not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({'error': 'Missing email, password or name'}),400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}),400

        user = User(email=data['email'],name=data['name'],role=data['role'])
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()
        
        print("User:",user)

        return jsonify({
            'message':'User Registered Successfully',
            'user': user.to_dict()
        }),201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500

@auth_bp.route('/login', methods=['POST'])
def login():
    """LOGIN USER AND RETURN JWT TOKEN"""
    try:
        data = request.get_json()

        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email or password not enterred'}),400
        
        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return jsonify({'error':'Invalid user email entererd'}),401
        if not user.check_password(data['password']):
            return jsonify({'error': 'Invalid Password enterred'}), 401

        token = generate_token(user.id)

        return jsonify({
            'message': 'Login Successful',
            'token': token,
            'user': user.to_dict()
        }),200
    except Exception as e:
        return jsonify({'error':str(e)}),500

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_me(current_user):
    """GET CURRENT USER"""
    try:
        print('current_user',current_user)
        return jsonify({'current_user':current_user.id}),200
    except Exception as e:
        return jsonify({'error': str(e)}),500