from flask import Blueprint

auth_bp = Blueprint('auth',__name__)
categories_bp = Blueprint('categories',__name__)
products_bp = Blueprint('products',__name__)
sales_bp = Blueprint('sales',__name__)

from app.routes.auth import *
from app.routes.products import *
from app.routes.categories import *