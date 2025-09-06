from flask import Flask, render_template, redirect, url_for, request, flash, session
from models import db, User, Customer, Product, Sale, Invoice
from config import Config
from forms import LoginForm, ChangePasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from forms import UpdateAccountForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# -------------------- Auth --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# -------------------- Change Password --------------------
@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = ChangePasswordForm()
    user = User.query.get(session['user_id'])

    if form.validate_on_submit():
        if not check_password_hash(user.password, form.current_password.data):
            flash('Current password is incorrect')
        else:
            user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Password updated successfully')
            return redirect(url_for('dashboard'))

    return render_template('change_password.html', form=form)

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
from forms import UpdateAccountForm

@app.route('/update-account', methods=['GET', 'POST'])
def update_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = UpdateAccountForm()
    user = User.query.get(session['user_id'])

    if form.validate_on_submit():
        if not check_password_hash(user.password, form.current_password.data):
            flash('Current password is incorrect')
        else:
            user.username = form.username.data
            user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Account updated successfully')
            return redirect(url_for('dashboard'))

    return render_template('update_account.html', form=form)

# -------------------- Init --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
