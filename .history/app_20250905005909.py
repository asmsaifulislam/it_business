from flask import Flask, render_template, redirect, url_for, request, flash, session
from models import db, User, Customer, Product, Sale, Invoice
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# -------------------- Auth --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# -------------------- Dashboard --------------------
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

# -------------------- Customers --------------------
@app.route('/customers')
def customers():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    all_customers = Customer.query.all()
    return render_template('customers.html', customers=all_customers)

# -------------------- Products --------------------
@app.route('/products')
def products():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

# -------------------- Sales --------------------
@app.route('/sales')
def sales():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    all_sales = Sale.query.all()
    return render_template('sales.html', sales=all_sales)

# -------------------- Invoices --------------------
@app.route('/invoice')
def invoice():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    all_invoices = Invoice.query.all()
    return render_template('invoice.html', invoices=all_invoices)

# -------------------- Reports --------------------
@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('reports.html')

# -------------------- Init --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
