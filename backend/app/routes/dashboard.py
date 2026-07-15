from flask import request, jsonify
from datetime import datetime,timedelta
from app.routes import dashboard_bp
from app.database import db
from app.models import Product, Category, Sale, User
from app.auth import token_required, admin_required

@dashboard_bp.route('/summary',methods=['GET'])
@token_required
def dashboard_summary(current_user):
    try:
        #step 1: Get todays date and month start date
        today = datetime.utcnow().date()
        month_start_date = today.replace(day=1)

        #step 2: Get Total Revenue
        total_revenue = db.session.query(db.func.sum(Sale.total_price)).scalar()
        if total_revenue  is None:
            total_revenue = 0

        #step 3: Get Monthly Revenue
        monthly_revenue = db.session.query(db.func.sum(Sale.total_price)).filter(db.func.date(Sale.created_at)>=month_start_date).scalar()
        if monthly_revenue  is None:
            monthly_revenue = 0

        #step 4: Get Total Products
        total_products = Product.query.count()

        #step 5: Get Low Stock Count
        low_stock_count = Product.query.filter(
            Product.stock_quantity<= Product.low_stock_threshold
        ).count()

        #step 6: Get sales made today
        sales_today = Sale.query.filter(
            db.func.date(Sale.created_at) == today
        ).count()


        #total_revenue = """ db.session.query(db.func.sum(Sale.total_price)).scalar() or 0 """
        #monthly_revenue = """db.session.query(db.func.sum(Sale.total_price)).scalar().filter_by(date(mm)) or 0 """
        #total_products = """Product.query.count()"""
        #low_stock_count = """count where stock<=threshold"""
        #sales_today = """count where date = today"""

        return jsonify({
            'total_revenue' : total_revenue,
            'monthly_revenue' : monthly_revenue,
            'total_products' : total_products,
            'low_stock_count' : low_stock_count,
            'sales_today' : sales_today 
        }),200

    except Exception as e:
        return jsonify({'error': str(e)}),500


@dashboard_bp.route('/revenue-by-day',methods=['GET'])
@token_required
def dashboard_revenue_by_day(current_user):
    try:
        # step 1: Calculate 30 days ago
        thirty_days = datetime.utcnow() - timedelta(days=30)

        # step 2: Get sales data grouped by date
        last_30_days = db.session.query(
            db.func.date(Sale.created_at).label('date'),
            db.func.sum(Sale.total_price).label('revenue')
        ).filter(Sale.created_at>=thirty_days).group_by(
            db.func.date(Sale.created_at)
        ).order_by(
            db.func.date(Sale.created_at)
        ).all()
        print("last 30 days data:", last_30_days)
        # step 3: Get list of data from the above query
        dict_data = [
            {
                'date':str(row.date),
                'revenue': round(float(row.revenue),2)
            }
            for row in last_30_days
        ]
        
        print("Dict data:", dict_data)

        return jsonify(
            dict_data
            ),200

    except Exception as e:
        return jsonify({'error': str(e)}),500

@dashboard_bp.route('/top-products',methods=['GET'])
@token_required
def dashboard_top_products(current_user):
    try:

        # step 1: join sales and products table
        # step 2: group by product name
        # step 3: sum revenue by product
        # step 4: order by revenue descending
        # step 5: limit to 5

        top_products_query = db.session.query(
            Product.name.label('product'),
            db.func.sum(Sale.total_price).label('revenue')
        ).join(Sale,Sale.product_id == Product.id).group_by(
            Product.name
        ).order_by(db.func.sum(Sale.total_price).desc()).limit(5).all()


        # step 6: get list of the top products from above query
        top_products_dict=[
            {
                'product' : row.product,
                'revenue' : round(float(row.revenue),2)
            }
            for row in top_products_query
        ]

        return jsonify(top_products_dict)
    except Exception as e:
        return jsonify({'error': str(e)}),500

@dashboard_bp.route('/revenue-by-category',methods=['GET'])
@token_required
def dashboard_revenue_by_cat(current_user):
    try:

        # Step 1 : Join 3 tables: Category, Product and Sales
        # Step 2 : Group by Category name
        # Step 3 : Sum Revenue by category
        # Step 4 : Order by revenue descending
        revenue_by_cat_query = db.session.query(
            Category.name.label('category'),
            db.func.sum(Sale.total_price).label('revenue')
        ).join(Product, Product.category_id == Category.id
        ).join(Sale, Sale.product_id == Product.id
        ).group_by(Category.name).order_by(
            db.func.sum(Sale.total_price).desc()
        ).all()

        revenue_by_cat_dict = [
            {
                'category' : row.category,
                'revenue' : round(float(row.revenue),2) 
            }
            for row in revenue_by_cat_query
        ]

        return jsonify(revenue_by_cat_dict)
    except Exception as e:
        return jsonify({'error': str(e)}),500