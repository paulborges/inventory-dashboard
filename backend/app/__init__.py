from flask import Blueprint
from flask import Flask
from config import Config
from flask_cors import CORS
from app.database import db, init_db


def create_app():
    """CREATE and CONFIGURE THE FLASK APP"""

    app = Flask(__name__)

    app.config.from_object(Config)

    init_db(app)

    CORS(app)
    from app.routes import auth_bp,products_bp,categories_bp,sales_bp
    app.register_blueprint(auth_bp,url_prefix = '/api/auth')
    app.register_blueprint(categories_bp,url_prefix = '/api/categories')
    app.register_blueprint(products_bp,url_prefix = '/api/products')
    app.register_blueprint(sales_bp,url_prefix = '/api/sales')

    return app

