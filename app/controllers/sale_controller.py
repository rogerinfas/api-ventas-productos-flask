from flask import Blueprint, request, jsonify
from flask_babel import gettext as _
from flask_jwt_extended import jwt_required
from app import db
from app.models import Product, Sale

sale_bp = Blueprint('sale', __name__, url_prefix='/api')

@sale_bp.route('/sales', methods=['POST'])
@jwt_required()
def create_sale():
    data = request.json or {}
    product_id = data.get('product_id')
    
    try:
        quantity = int(data.get('quantity', 0))
    except ValueError:
        return jsonify({'error': _('Quantity must be an integer')}), 400
    
    if quantity <= 0:
        return jsonify({'error': _('Quantity must be greater than zero')}), 400
        
    try:
        # Bloqueo pesimista
        product = db.session.query(Product).filter_by(id=product_id).with_for_update().first()
        if not product:
            return jsonify({'error': _('Product not found')}), 404
            
        if product.stock < quantity:
            return jsonify({'error': _('Not enough stock')}), 400
            
        total_price = product.price * quantity
        
        product.stock -= quantity
        new_sale = Sale(product_id=product.id, quantity=quantity, total_price=total_price)
        db.session.add(new_sale)
        
        db.session.commit()
        return jsonify({'message': _('Sale registered successfully'), 'sale_id': new_sale.id}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': _('Failed to register sale: ') + str(e)}), 500
