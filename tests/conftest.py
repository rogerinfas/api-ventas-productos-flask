import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    
    with app.app_context():
        # Las tablas ya se habrán creado en create_app(), pero nos aseguramos
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    response = client.post('/api/login', json={
        "username": "admin",
        "password": "password"
    })
    token = response.get_json().get('access_token')
    return {'Authorization': f'Bearer {token}'}
