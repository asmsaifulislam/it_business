from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

db = SQLAlchemy()

# Product Table
class Product(db.Model):
    __tablename__ = 'product'

     id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    onboard_date = db.Column(db.Date, default=datetime.utcnow)

    # Relationships
    sales = db.relationship('Sale', back_populates='product', cascade='all, delete-orphan')


# Customer Table
class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(200))

    # Relationships
    sales = db.relationship('Sale', back_populates='customer', cascade='all, delete-orphan')


# Sale Table
class Sale(db.Model):
    __tablename__ = 'sale'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = db.relationship('Product', back_populates='sales')
    customer = db.relationship('Customer', back_populates='sales')
    invoice = db.relationship('Invoice', back_populates='sale', uselist=False, cascade='all, delete-orphan')


# Invoice Table
class Invoice(db.Model):
    __tablename__ = 'invoice'

    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False, unique=True)
    status = db.Column(db.String(20), default='Unpaid')

    # Relationships
    sale = db.relationship('Sale', back_populates='invoice')


# User Table (for login/admin)
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
