from wtforms.validators import DataRequired, Email, Length, EqualTo
from datetime import datetime
from . import db

# -------------------- User --------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)


# -------------------- Customer --------------------
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(20), nullable=True)

    # Relationship to Sale
    sales = db.relationship("Sale", back_populates="customer", cascade="all, delete-orphan")



# -------------------- Product --------------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    onboard_date = db.Column(db.Date, default=datetime.utcnow)

    # Relationship to Sale
    sales = db.relationship("Sale", back_populates="product", cascade="all, delete-orphan")



# -------------------- Sale --------------------

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    customer = db.relationship('Customer', back_populates='sales')
    product = db.relationship('Product', back_populates='sales')
    invoices = db.relationship('Invoice', back_populates='sale', cascade="all, delete-orphan")




# -------------------- Invoice --------------------

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)      # Invoice ID
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    customer = db.Column(db.String(120), nullable=False)
    product = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)

    sale = db.relationship('Sale', backref=db.backref('invoices', lazy=True))
    # Relationship to Sale
    sale = db.relationship('Sale', back_populates='invoices')