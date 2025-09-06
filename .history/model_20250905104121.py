class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    # 👇 Add this line to fix the error
    stock = db.Column(db.Integer, default=0)
