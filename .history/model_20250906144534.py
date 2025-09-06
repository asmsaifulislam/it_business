from datetime import datetime
from . import db  # make sure this imports your SQLAlchemy instance

# -------------------- User --------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)


# -------------------- Customer --------------------
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    mobile = db.Column(db.String(20), unique=True, nullable=True)  # ✅ Added mobile column


# -------------------- Product --------------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    onboard_date = db.Column(db.Date, default=datetime.utcnow)  # keep it simple


# -------------------- Sale --------------------
  id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)

    # Relationships
    customer = db.relationship("Customer", back_populates="sales")
    product = db.relationship("Product", back_populates="sales")


# -------------------- Invoice --------------------
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    status = db.Column(db.String(20), default='Unpaid')
