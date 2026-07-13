from datetime import datetime
from app.database import db
import bcrypt

class User(db.Model):
    __tablename__='Users'

    id = db.Column(db.Integer, primary_key = True)
    name= db.Column(db.String(120),nullable=False)
    email= db.Column(db.String(120),unique=True,nullable=False,index=True)
    password_hash= db.Column(db.String(255),nullable=False)
    role= db.Column(db.String, default='staff')
    created_at= db.Column(db.DateTime,default=datetime.utcnow)

    def set_password(self,password):
        """HASH PASSWORD WITH BCRYPT"""
        self.password_hash=bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self,password):
        """CHECK IF PASSWORD MATCHES WITH HASH"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'role': self.role,
            'created_at':self.created_at.isoformat()
        }

class Category(db.Model):
    __tablename__ = 'Categories'

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), unique = True, nullable= True) 
    description = db.Column(db.String(300), nullable= True)

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Product(db.Model):
    __tablename__ = 'Product'
    
    id = db.Column(db.Integer, primary_key= True)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable=False, index= True)
    name = db.Column(db.String(100), unique = True, nullable= False)
    description = db.Column(db.String(300), nullable= True)
    price = db.Column(db.Integer, nullable= False)
    stock = db.Column(db.Integer, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    low_stock_threshold = db.Column(db.Integer, nullable= True)
    sku = db.Column(db.Integer, unique = True)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    
    def is_low_stock():
        if stock <= low_stock_threshold:
            return True
    

    def to_dict(self):
        return{
            'id': self.id,
            'category_id': self.category_id.to_dict(),
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'quantity': self.quantity,
            'low_stock_threshold': self.low_stock_threshold,
            'low_stock': self.is_low_stock(),
            'sku':self.sku,
            'created_at': self.created_at.isoformat()
        }

class Sale(db.Model):
    __tablename__ = 'Sales'

    id = db.Column(db.Integer, primary_key= True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'), nullable=False, index= True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False, index= True)
    quantity =db.Column(db.Integer, nullable = False)
    unit_price = db.Column(db.Integer, nullable = False)
    total_price = db.Column(db.Integer, nullable = False)
    notes = db.Column(db.String(300), nullable= True)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    def to_dict(self):
        return{
            'id': self.id,
            'product_id': self.product_id.to_dict(),
            'user_id': self.user_id,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_price': self.total_price,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }