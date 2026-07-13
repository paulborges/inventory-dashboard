from flask import request,jsonify
from app.routes import categories_bp
from app.database import db
from app.models import Category
from app.auth import token_required
from app.auth import admin_required

@categories_bp.route('',methods=['GET'])
@admin_required

def get_categories(current_user):
    """GET ALL CATEGORIES"""
    try:
        categories = Categories.query.all()

        return jsonify({
            'categories': [c.to_dict() for c in categories]
        }),200
    except Exception as e:
        return jsonify({'error':str(e)}),500

@categories_bp.route('',methods=['POST'])
@admin_required

def create_categories(current_user):
    """CREATE CATEGORY"""
    try:
        data = request.get_json()

        if not data or not data.get('name'):
            return jsonify({'error':'Missing Category Name'}),400
        
        if Category.query.filter_by(name=data['name'],).first():
            return jsonify({'error':'Category already exists'}),400
        
        category=Category(
            name = data['name'],
            description = data.get('description','')
        )

        db.session.add(category)
        db.session.commit()

        return jsonify({
            'message':'Category Created',
            'category':category.to_dict()
        })


    except Exception as e:
        return jsonify({'error':str(e)}),500