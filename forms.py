from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# -------------------- Login Form --------------------
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired()])
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
    mobile = StringField(
        'Mobile Number',
        validators=[DataRequired(), Length(min=6, max=20)],
        render_kw={"placeholder": "Enter mobile number"}
    )
    submit = SubmitField('Add Customer')

# -------------------- Product Form --------------------
class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    stock = IntegerField('Quantity', validators=[DataRequired()])
    onboard_date = DateField('Onboard Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Product')


# -------------------- Sale Form --------------------
class SaleForm(FlaskForm):
    customer_id = SelectField('Select Customer', coerce=int, validators=[DataRequired()])
    product_id = SelectField('Select Product', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Record Sale')


# -------------------- Invoice Form --------------------
class InvoiceForm(FlaskForm):
    sale_id = SelectField('Select Sale', coerce=int, validators=[DataRequired()])
    status = SelectField('Status', choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], validators=[DataRequired()])
    submit = SubmitField('Generate Invoice')


# -------------------- Change Password Form --------------------
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Change Password')


# -------------------- Update Account Form --------------------
class UpdateAccountForm(FlaskForm):
    username = StringField('New Username', validators=[DataRequired(), Length(min=3)])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Update Account')
