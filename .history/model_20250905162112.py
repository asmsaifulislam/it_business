from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
TypeError
TypeError: 'onboard_date' is an invalid keyword argument for Product

Traceback (most recent call last)
File "C:\Users\saifu\OneDrive\Desktop\it_business_tool\venv\Lib\site-packages\flask\app.py", line 1536, in __call__
return self.wsgi_app(environ, start_response)
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\saifu\OneDrive\Desktop\it_business_tool\venv\Lib\site-packages\flask\app.py", line 1514, in wsgi_app
response = self.handle_exception(e)
           ^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\saifu\OneDrive\Desktop\it_business_tool\venv\Lib\site-packages\flask\app.py", line 1511, in wsgi_app
response = self.full_dispatch_request()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\saifu\OneDrive\Desktop\it_business_tool\venv\Lib\site-packages\flask\app.py", line 919, in full_dispatch_request
rv = self.handle_user_exception(e)
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\saifu\OneDrive\Desktop\it_business_tool\venv\Lib\site-packages\flask\app.py", line 917, in full_dispatch_request
rv = self.dispatch_request()
     ^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\saifu\OneDrive\Desktop\it_business_tool\venv\Lib\site-packages\flask\app.py", line 902, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "c:\Users\saifu\OneDrive\Desktop\it_business_tool\app.py", line 146, in add_product
new_product = Product(
              
File "<string>", line 4, in __init__
File "C:\Users\saifu\OneDrive\Desktop\it_business_tool\venv\Lib\site-packages\sqlalchemy\orm\state.py", line 571, in _initialize_instance
with util.safe_reraise():
     ^^^^^^^^^^^^^^^^^^^
File "C:\Users\saifu\OneDrive\Desktop\it_business_tool\venv\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 224, in __exit__
raise exc_value.with_traceback(exc_tb)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\saifu\OneDrive\Desktop\it_business_tool\venv\Lib\site-packages\sqlalchemy\orm\state.py", line 569, in _initialize_instance
manager.original_init(*mixed[1:], **kwargs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\saifu\OneDrive\Desktop\it_business_tool\venv\Lib\site-packages\sqlalchemy\orm\decl_base.py", line 2179, in _declarative_constructor
raise TypeError(
^
TypeError: 'onboard_date' is an invalid keyword argument for Product
The debugger caught an exception in your WSGI application. You can now look at the traceback which led to the error.
To switch between the interactive traceback and the plaintext one, you can click on the "Traceback" headline. From the text traceback you can also create a paste of it. For code execution mouse-over the frame you want to debug and click on the console icon on the right side.

You can execute arbitrary Python code in the stack frames and there are some extra helpers available for introspection:

dump() shows all variables in the frame
dump(obj) dumps all that's known about the object


db = SQLAlchemy()

# Product Table
class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    onboard_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

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
