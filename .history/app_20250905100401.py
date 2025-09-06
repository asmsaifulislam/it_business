from flask import Flask, render_template, redirect, url_for, request, flash, session
from config import Config
from models import db, User, Customer, Product, Sale, Invoice
from forms import (
    LoginForm,
    ChangePasswordForm,
    UpdateAccountForm,
    CustomerForm,
    ProductForm,
    SaleForm,
    InvoiceForm
)
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------- App Setup --------------------
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# -------------------- One-Time Admin Creation --------------------
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()

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

# -------------------- Update Account --------------------
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

# -------------------- Add Product --------------------
@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = ProductForm()
    if form.validate_on_submit():
        try:
            new_product = Product(name=form.name.data, price=form.price.data)
            db.session.add(new_product)
            db.session.commit()
            flash('✅ Product added successfully', 'success')
            return redirect(url_for('products'))
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error adding product: {str(e)}', 'danger')

    return render_template('add_product.html', form=form)

# -------------------- Record Sale --------------------
@app.route('/record-sale', methods=['GET', 'POST'])
def record_sale():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = SaleForm()
    form.customer_id.choices = [(c.id, c.name) for c in Customer.query.all()]
    form.product_id.choices = [(p.id, p.name) for p in Product.query.all()]

    if form.validate_on_submit():
        product = Product.query.get(form.product_id.data)
        total = product.price * form.quantity.data
        new_sale = Sale(
            customer_id=form.customer_id.data,
            product_id=form.product_id.data,
            quantity=form.quantity.data,
            total=total
        )
        db.session.add(new_sale)
        db.session.commit()
        flash('Sale recorded successfully')
        return redirect(url_for('sales'))

    return render_template('record_sale.html', form=form)
#------------------sales report-----------------------
@app.route('/sales-report')
def sales_report():
    # Fetch and render sales data
    return render_template('sales_report.html')


# -------------------- Create Invoice (Manual Form) --------------------
@app.route('/create-invoice', methods=['GET', 'POST'])
def create_invoice():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = InvoiceForm()
    form.sale_id.choices = [(sale.id, f"Sale #{sale.id} - {sale.customer.name}") for sale in Sale.query.all()]

    if form.validate_on_submit():
        sale = Sale.query.get_or_404(form.sale_id.data)
        existing_invoice = Invoice.query.filter_by(sale_id=sale.id).first()
        if existing_invoice:
            flash('Invoice already exists for this sale.', 'warning')
        else:
            new_invoice = Invoice(sale_id=sale.id, status=form.status.data)
            db.session.add(new_invoice)
            db.session.commit()
            flash('Invoice created successfully.', 'success')
        return redirect(url_for('invoice'))

    return render_template('create_invoice.html', form=form)

# -------------------- Generate Invoice (Auto from Sale) --------------------
@app.route('/generate-invoice/<int:sale_id>', methods=['POST'])
def generate_invoice(sale_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    sale = Sale.query.get_or_404(sale_id)
    existing_invoice = Invoice.query.filter_by(sale_id=sale.id).first()
    if existing_invoice:
        flash('Invoice already exists for this sale.', 'warning')
    else:
        new_invoice = Invoice(sale_id=sale.id, status='Unpaid')
        db.session.add(new_invoice)
        db.session.commit()
        flash('Invoice generated successfully.', 'success')

    return redirect(url_for('invoice'))

# -------------------- Mark Invoice as Paid --------------------
@app.route('/mark-paid/<int:invoice_id>', methods=['POST'])
def mark_paid(invoice_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    invoice = Invoice.query.get_or_404(invoice_id)
    invoice.status = 'Paid'
    db.session.commit()
    flash('Invoice marked as paid.', 'success')
    return redirect(url_for('invoice'))

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

@app.route('/add-customer', methods=['GET', 'POST'])
def add_customer():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    form = CustomerForm()
    if form.validate_on_submit():
        new_customer = Customer(name=form.name.data, email=form.email.data)
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer added successfully')
        return redirect(url_for('customers'))

    return render_template('add_customer.html', form=form)

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
# -------------------- Sales Report --------------------


# -------------------- Customer Report --------------------
@app.route('/customer-report')
def customer_report():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('customer_report.html')

# -------------------- Product Report --------------------
@app.route('/product-report')
def product_report():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('product_report.html')

# -------------------- Invoice Report --------------------
@app.route('/invoice-report')
def invoice_report():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('invoice_report.html')

# -------------------- Run --------------------
if __name__ == '__main__':
    app.run(debug=True)
