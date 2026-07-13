from flask import request, jsonify
from datetime import datetime
from app.routes import products_bp
from app.database import db
from app.models import Product,Category
from app.auth import token_required
from app.auth import admin_required

@products_bp.route('',methods=['GET'])
@token_required

def get_products(current_user):
    """GET ALL PRODUCTS"""
    try:
        products = Product.query.all()

        search = request.args.get('search') 
        if search:
            products = Product.query.filter(Product.name.ilike(f"%{search}%")).all()
 
        category_id = request.args.get('category_id')
        if category_id:
            products = Product.query.filter_by(category_id=category_id).all()

        return jsonify({
            'products': [p.to_dict() for p in products]
        }),200
    except Exception as e:
        return jsonify({'error': str(e)}),500

@products_bp.route('low-stock',methods=['GET'])
@token_required

def get_low_stock(current_user):
    """GET LOW STOCK"""
    try:
        products= Product.query.filter(Product.stock_quantity<=Product.low_stock_threshold).all()
        return jsonify({
            'Low products': [p.to_dict() for p in products]
        }),200
    except Exception as e:
        return jsonify({'error': str(e)}),500


@products_bp.route('',methods=['POST'])
@admin_required
def create_product(current_user):
    """CREATE NEW PRODUCT INFORMATION"""
    try:
        data= request.get_json()
        print("data:",data)
        if not data or not data.get('category_id') or not data.get('product_name') or not data.get('product_price') or not data.get('product_quantity') or not data.get('product_sku'):
            return jsonify({'error':'Missing information'}),400

        
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({'error':'Category not found'}),404
        
        product = Product(
            category_id = data['category_id'],
            name = data['product_name'],
            description = data.get('product_desc',''),
            price = data['product_price'],
            stock_quantity = data['product_quantity'],
            low_stock_threshold = data['product_low_stock_thresh'],
            sku = data['product_sku'],
            created_at = data.get('date',datetime.utcnow().date()) 
        )

        print("Product: ",product)

        db.session.add(product)
        db.session.commit()

        return jsonify({
            'message':'Product Created Successfully',
            'product':product.to_dict()
            }),201
    except Exception as e:
        db.session.rollback
        return jsonify({'error':str(e)}),500

@products_bp.route('/<int:id>',methods=['PUT'])
@admin_required

def put_product(current_user,id):
    """UPDATE PRODUCT INFORMATION"""
    try:
        product = Product.query.filter_by(id=id).first()

        if not product:
            return jsonify({
                'error':'Product not found'
            }),404

        data = request.get_json()


        if 'category_id' in data:
            category=Category.query.get(data['category_id'])
            if not category:
                return jsonify({'error':'Category not found'}),404
            product.category_id=data['category_id']

        if 'description' in data:
            product.description=data['product_desc']
        
        if 'price' in data:
            product.description=data['product_price']
        
        if 'stock' in data:
            product.description=data['product_stock']
        
        if 'quantity' in data:
            product.description=data['product_quantity']

        if 'low_stock_threshold' in data:
            product.description=data['product_low_stock_thresh']
        
        if 'date' in data:
            product.date=data['date']

        db.session.commit()


        return jsonify({
            'message':'Product updated',
            'products': product.to_dict()
        }),200
    except Exception as e:
        db.session.rollback
        return jsonify({'error':str(e)}),500
 

@products_bp.route('/<id>',methods=['DELETE'])
@admin_required

def delete_product(current_user,id):
    """DELETE A PRODUCT FROM DATABASE"""
    try:
        product = Product.query.filter_by(id=id).first()

        if not product:
            return jsonify({'error':str(e)}),404
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message':'Product deleted'}),200

    except Exception as e:
        db.session.rollback
        return jsonify({'error': str(e)}),500