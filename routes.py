from flask import Blueprint, request, jsonify, current_app
from flask_babel import gettext as _
from app import db
from models import Product, Sale
from sqlalchemy.exc import IntegrityError

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
    data = request.json or {}
    
    try:
        price_raw = data.get('price')
        stock_raw = data.get('stock')
        
        # Intentar convertir valores numéricos antes de instanciar para un error controlado
        price = float(price_raw) if price_raw is not None else None
        stock = int(stock_raw) if stock_raw is not None else None

        # La validación Regex se ejecuta automáticamente al instanciar mediante @validates de SQLAlchemy
        new_product = Product(
            sku=data.get('sku'),
            name=data.get('name'),
            price=price,
            stock=stock
        )
        
        db.session.add(new_product)
        db.session.commit() # Confirmar transacción
        
        return jsonify({'message': _('Product created successfully'), 'id': new_product.id}), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': _('Product with this SKU already exists')}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': _('Failed to create product: ') + str(e)}), 500

@api_bp.route('/sales', methods=['POST'])
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
        # Bloqueo pesimista (SELECT FOR UPDATE) para evitar condiciones de carrera en concurrencia
        product = db.session.query(Product).filter_by(id=product_id).with_for_update().first()
        if not product:
            return jsonify({'error': _('Product not found')}), 404
            
        if product.stock < quantity:
            return jsonify({'error': _('Not enough stock')}), 400
            
        total_price = product.price * quantity
        
        # Control de transacciones
        product.stock -= quantity
        new_sale = Sale(product_id=product.id, quantity=quantity, total_price=total_price)
        db.session.add(new_sale)
        
        db.session.commit()
        return jsonify({'message': _('Sale registered successfully'), 'sale_id': new_sale.id}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': _('Failed to register sale: ') + str(e)}), 500
