import jwt
from datetime import datetime,timedelta
from functools import wraps
from flask import request, jsonify, current_app
from app.models import User


def generate_token(user_id):
    """CREATE A JWT TOKEN FOR USER ID"""
    payload={
        'user_id':user_id,
        'exp': datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRATION_HOURS']),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload,current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def decode_token(token):
    """VERIFY AND DECODE JWT TOKEN"""
    
    try:
        
        payload = jwt.decode(token,current_app.config['SECRET_KEY'],algorithms='HS256')
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """DECORATOR TO PROTECT ROUTES WITH JWT AUTHENTICATION"""
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            parts = auth_header.split()
            if len(parts)== 2 and parts[0]=='Bearer':
                token = parts[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        user_id = decode_token(token)
        if user_id is None: 
            return jsonify({'error':'Token provided is invalid or missing'}), 401
        
        user = User.query.get(user_id)
        print("USER:",user)

        if not user:
            return jsonify({'error': 'User Not Found'}),401

        return f(current_user =user, *args, **kwargs)
    return decorated


def admin_required(f):
    """DECORATOR TO CHECK FOR ADMIN USER"""
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            parts = auth_header.split()
            if len(parts)== 2 and parts[0]=='Bearer':
                token = parts[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        user_id = decode_token(token)
        if user_id is None: 
            return jsonify({'error':'Token is invalid or missing'}), 401
        
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User Not Found'}),401

        if not user.role == 'admin':
            return jsonify({'error': 'Admin access required'}), 401

        return f(current_user =user, *args, **kwargs)
    return decorated
        