# -------------------- Core Imports --------------------
import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# -------------------- Load Environment Variables --------------------
load_dotenv()

# -------------------- Config --------------------
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# -------------------- App Initialization --------------------
app = Flask(__name__)
app.config.from_object(Config)

# -------------------- Database --------------------
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# -------------------- Models --------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    status = db.Column(db.String(20), default='Unpaid')

# -------------------- One-Time Admin Creation --------------------
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()

# -------------------- Routes --------------------
@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    stats = {
        'customers': Customer.query.count(),
        'products': Product.query.count(),
        'sales': Sale.query.count(),
        'invoices': Invoice.query.count()
    }
    return render_template('dashboard.html', stats=stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/product-report')
def product_report():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    total_products = Product.query.count()
    low_stock = Product.query.filter(Product.stock < 10).all()
    return render_template('product_report.html', total_products=total_products, low_stock=low_stock)

# -------------------- Run --------------------
if __name__ == '__main__':
    app.run(debug=True)

# -------------------- Invoice Report --------------------
@app.route('/invoice-report')
def invoice_report():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    total_invoices = Invoice.query.count()
    paid = Invoice.query.filter_by(status='Paid').count()
    unpaid = Invoice.query.filter_by(status='Unpaid').count()
    overdue = Invoice.query.filter_by(status='Overdue').count()

    return render_template('invoice_report.html',
                           total_invoices=total_invoices,
                           paid=paid,
                           unpaid=unpaid,
                           overdue=overdue)


# -------------------- Run --------------------
if __name__ == '__main__':
    app.run(debug=True)
