from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from datetime import datetime

# -------------------- Login Form --------------------
class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3)],
        render_kw={"placeholder": "Enter username"}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password"}
    )
    submit = SubmitField('Login')

# -------------------- Customer Form --------------------
class CustomerForm(FlaskForm):
    name = StringField(
        'Customer Name',
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter full name"}
    )
    email = StringField(
        'Email Address',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Enter email"}
    )
    submit = SubmitField('Add Customer')

# -------------------- Product Form --------------------
class ProductForm(FlaskForm):
    name = StringField(
        'Product Name',
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter product name"}
    )
    price = FloatField(
        'Price ($)',
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter price"}
    )
    stock = IntegerField(  # ✅ New field
        'Quantity',
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter quantity"}
    )
    onboard_date = DateField(  # ✅ New field
        'Onboard Date',
        format="%Y-%m-%d",
        default=datetime.utcnow,
        render_kw={"placeholder": "YYYY-MM-DD"}
    )
    submit = SubmitField('Add Product')

# -------------------- Sale Form --------------------
class SaleForm(FlaskForm):
    customer_id = SelectField('Select Customer', coerce=int, validators=[DataRequired()])
    product_id = SelectField('Select Product', coerce=int, validators=[DataRequired()])
    quantity = IntegerField(
        'Quantity',
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter quantity"}
    )
    submit = SubmitField('Record Sale')

# -------------------- Invoice Form --------------------
class InvoiceForm(FlaskForm):
    sale_id = SelectField('Select Sale', coerce=int, validators=[DataRequired()])
    status = SelectField(
        'Status',
        choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Generate Invoice')

# -------------------- Change Password Form --------------------
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        'Current Password',
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter current password"}
    )
    new_password = PasswordField(
        'New Password',
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter new password"}
    )
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(),
            EqualTo('new_password', message='Passwords must match')
        ],
        render_kw={"placeholder": "Confirm new password"}
    )
    submit = SubmitField('Change Password')

# -------------------- Update Account Form --------------------
class UpdateAccountForm(FlaskForm):
    username = StringField(
        'New Username',
        validators=[DataRequired(), Length(min=3)],
        render_kw={"placeholder": "Enter new username"}
    )
    current_password = PasswordField(
        'Current Password',
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter current password"}
    )
    new_password = PasswordField(
        'New Password',
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter new password"}
    )
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(),
            EqualTo('new_password', message='Passwords must match')
        ],
        render_kw={"placeholder": "Confirm new password"}
    )
    submit = SubmitField('Update Account')
