import time
import pytest
from app import db
from models import Product

def simulate_delay():
    # Retraso simulado para evidenciar visualmente el paralelismo en la ejecución
    time.sleep(1)

def test_create_product_success(client, auth_headers):
    simulate_delay()
    response = client.post('/api/products', headers=auth_headers, json={
        "sku": "ABC1234",
        "name": "Teclado Mecanico",
        "price": 89.99,
        "stock": 50
    })
    assert response.status_code == 201
    assert "id" in response.get_json()

def test_create_product_invalid_sku(client, auth_headers):
    simulate_delay()
    response = client.post('/api/products', headers=auth_headers, json={
        "sku": "invalid-sku",
        "name": "Teclado Mecanico",
        "price": 89.99,
        "stock": 50
    })
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_product_invalid_name(client, auth_headers):
    simulate_delay()
    response = client.post('/api/products', headers=auth_headers, json={
        "sku": "ABC1234",
        "name": "Teclado @ Mecanico",
        "price": 89.99,
        "stock": 50
    })
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_product_negative_price(client, auth_headers):
    simulate_delay()
    response = client.post('/api/products', headers=auth_headers, json={
        "sku": "ABC1234",
        "name": "Teclado Mecanico",
        "price": -10.00,
        "stock": 50
    })
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_product_negative_stock(client, auth_headers):
    simulate_delay()
    response = client.post('/api/products', headers=auth_headers, json={
        "sku": "ABC1234",
        "name": "Teclado Mecanico",
        "price": 89.99,
        "stock": -5
    })
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_sale_success(client, app, auth_headers):
    simulate_delay()
    # Insertar producto inicial
    with app.app_context():
        p = Product(sku="XYZ9876", name="Mouse Gamer", price=25.00, stock=10)
        db.session.add(p)
        db.session.commit()
        product_id = p.id

    response = client.post('/api/sales', headers=auth_headers, json={
        "product_id": product_id,
        "quantity": 3
    })
    assert response.status_code == 201
    
    # Verificar stock restante
    with app.app_context():
        updated_product = db.session.get(Product, product_id)
        assert updated_product.stock == 7

def test_create_sale_insufficient_stock(client, app, auth_headers):
    simulate_delay()
    with app.app_context():
        p = Product(sku="XYZ9876", name="Mouse Gamer", price=25.00, stock=2)
        db.session.add(p)
        db.session.commit()
        product_id = p.id

    response = client.post('/api/sales', headers=auth_headers, json={
        "product_id": product_id,
        "quantity": 5
    })
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_sale_invalid_quantity(client, app, auth_headers):
    simulate_delay()
    with app.app_context():
        p = Product(sku="XYZ9876", name="Mouse Gamer", price=25.00, stock=10)
        db.session.add(p)
        db.session.commit()
        product_id = p.id

    response = client.post('/api/sales', headers=auth_headers, json={
        "product_id": product_id,
        "quantity": -2
    })
    assert response.status_code == 400
    assert "error" in response.get_json()
