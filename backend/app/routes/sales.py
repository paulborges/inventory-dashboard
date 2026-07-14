from flask import request, jsonify
from datetime import datetime
from app.routes import sales_bp
from app.database import db
from app.models import Product, Category, Sale, User
from app.auth import token_required, admin_required

@sales_bp.route('',methods=['POST'])
@token_required
def create_sale(current_user):
    """CREATE NEW SALES RECORD"""
    try:
        data=request.get_json()
    
        if not data or not data.get('product_id') or not data.get('product_quantity'):
            return jsonify({'error':'Missing information'}),400
        
        product= Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error':'Product not found in database'}),404

        

        present_stock = product.stock_quantity
        if present_stock<data['product_quantity']:
            return jsonify({'error':f'Not enough stock present for current sale. Present Stock available: {present_stock}'}),400
        
        unit_price = product.price
        total_price = data['product_quantity']*unit_price
        curr_sale=Sale(
            product_id = data['product_id'],
            user_id = current_user.id,
            quantity = data['product_quantity'],
            unit_price = unit_price,
            total_price = total_price,
            notes = data.get('notes',''),
            created_at = data.get('date',datetime.utcnow().date())
        )
    
        db.session.add(curr_sale)
        product.stock_quantity = product.stock_quantity - data['product_quantity']
        db.session.commit()

        return jsonify({
            'message':'Sale Created Successfully',
            'sale': curr_sale.to_dict()
        }),201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500

@sales_bp.route('',methods=['GET'])
@token_required
def get_sales(current_user):
    """GET SALES """
    try:
        if current_user.role == 'admin':
            sales_query = Sale.query.all() 
        else:
            sales_query = Sale.query.filter_by(user_id = current_user.id)
        return jsonify({
            'sales':[s.to_dict() for s in sales_query]
        }),200

    except Exception as e:
        return jsonify({'error':str(e)}),500

@sales_bp.route('/my-sales',methods=['GET'])
@token_required
def my_sales(current_user):
    """GET CURRENT USER SALES """
    try:
        sales= Sale.query.filter_by(user_id = current_user.id)
        return jsonify({
            'sales':[s.to_dict() for s in sales]
        }),200

    except Exception as e:
        return jsonify({'error':str(e)}),500
