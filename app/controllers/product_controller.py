from flask import Blueprint, request, jsonify
from flask_babel import gettext as _
from flask_jwt_extended import jwt_required
from app import db
from app.models import Product
from sqlalchemy.exc import IntegrityError

product_bp = Blueprint('product', __name__, url_prefix='/api')

@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'sku': p.sku,
        'name': p.name,
        'price': float(p.price),
        'stock': p.stock
    } for p in products])

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.json or {}
    
    try:
        price_raw = data.get('price')
        stock_raw = data.get('stock')
        
        price = float(price_raw) if price_raw is not None else None
        stock = int(stock_raw) if stock_raw is not None else None

        new_product = Product(
            sku=data.get('sku'),
            name=data.get('name'),
            price=price,
            stock=stock
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({'message': _('Product created successfully'), 'id': new_product.id}), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': _('Product with this SKU already exists')}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': _('Failed to create product: ') + str(e)}), 500
