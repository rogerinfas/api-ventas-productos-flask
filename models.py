import re
from app import db
from datetime import datetime
from flask_babel import gettext as _

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)

    @staticmethod
    def validate_sku(sku):
        # Regex para asegurar que el SKU sea exactamente 3 letras mayúsculas seguidas de 4 dígitos (ej. ABC1234)
        if not re.match(r'^[A-Z]{3}\d{4}$', sku):
            raise ValueError(_("Invalid SKU format. Must be 3 uppercase letters followed by 4 digits (e.g., ABC1234)."))
        return sku

    @staticmethod
    def validate_name(name):
        # Regex para asegurar que el nombre contenga solo letras, números y espacios
        if not re.match(r'^[A-Za-z0-9\s]+$', name):
            raise ValueError(_("Name can only contain letters, numbers, and spaces."))
        return name

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
