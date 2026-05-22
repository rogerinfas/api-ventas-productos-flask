from flask import Blueprint, request, jsonify, current_app
from flask_babel import gettext as _
from app import db
from models import Product, Sale

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'sku': p.sku,
        'name': p.name,
        'price': float(p.price),
        'stock': p.stock
    } for p in products])

@api_bp.route('/products', methods=['POST'])
def create_product():
    data = request.json
    
    try:
        # Regex validation applied
        sku = Product.validate_sku(data.get('sku', ''))
        name = Product.validate_name(data.get('name', ''))
        price = float(data.get('price', 0))
        stock = int(data.get('stock', 0))
        
        # Transaction control start
        new_product = Product(sku=sku, name=name, price=price, stock=stock)
        db.session.add(new_product)
        db.session.commit() # Commit transaction
        
        return jsonify({'message': _('Product created successfully'), 'id': new_product.id}), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback() # Rollback transaction on failure
        if 'psycopg2.errors.UniqueViolation' in str(e) or 'UniqueViolation' in str(e) or 'unique constraint' in str(e).lower():
            return jsonify({'error': _('Product with this SKU already exists')}), 400
        return jsonify({'error': _('Failed to create product: ') + str(e)}), 500

@api_bp.route('/sales', methods=['POST'])
def create_sale():
    data = request.json
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 0))
    
    if quantity <= 0:
        return jsonify({'error': _('Quantity must be greater than zero')}), 400
        
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': _('Product not found')}), 404
            
        if product.stock < quantity:
            return jsonify({'error': _('Not enough stock')}), 400
            
        total_price = product.price * quantity
        
        # Transaction control
        product.stock -= quantity
        new_sale = Sale(product_id=product.id, quantity=quantity, total_price=total_price)
        db.session.add(new_sale)
        
        db.session.commit()
        return jsonify({'message': _('Sale registered successfully'), 'sale_id': new_sale.id}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': _('Failed to register sale: ') + str(e)}), 500
