from app import db
from datetime import datetime, timezone

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
