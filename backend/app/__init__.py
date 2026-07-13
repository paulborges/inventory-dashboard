from flask import Blueprint
from flask import Flask
from config import Config
from flask_cors import CORS
from app.database import db, init_db


auth_bp = Blueprint('auth',__name__)
categories_bp = Blueprint('categories',__name__)
products_bp = Blueprint('products',__name__)
sales_bp = Blueprint('sales',__name__)

def create_app():
    """CREATE and CONFIGURE THE FLASK APP"""

    app = Flask(__name__)

    app.config.from_object(Config)

    init_db(app)

    CORS(app)

    app.register_blueprint(auth_bp,url_prefix = '/api/auth')
    app.register_blueprint(categories_bp,url_prefix = '/api/categories')
    app.register_blueprint(products_bp,url_prefix = '/api/products')
    app.register_blueprint(sales_bp,url_prefix = '/api/sales')

    return app

