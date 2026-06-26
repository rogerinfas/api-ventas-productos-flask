import re
from app import db
from flask_babel import gettext as _
from sqlalchemy.orm import validates

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)

    @validates('sku')
    def validate_sku(self, key, sku):
        if not re.match(r'^[A-Z]{3}\d{4}$', sku or ''):
            raise ValueError(_("Invalid SKU format. Must be 3 uppercase letters followed by 4 digits (e.g., ABC1234)."))
        return sku

    @validates('name')
    def validate_name(self, key, name):
        if not re.match(r'^[A-Za-z0-9\s]+$', name or ''):
            raise ValueError(_("Name can only contain letters, numbers, and spaces."))
        return name

    @validates('price')
    def validate_price(self, key, price):
        if price is None or float(price) < 0:
            raise ValueError(_("Price must be a non-negative number."))
        return price

    @validates('stock')
    def validate_stock(self, key, stock):
        if stock is None or int(stock) < 0:
            raise ValueError(_("Stock must be a non-negative integer."))
        return stock
