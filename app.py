import os
from flask import Flask, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
babel = Babel()
jwt = JWTManager()

def get_locale():
    # Si el usuario ha iniciado sesión, podrías devolver su idioma de preferencia
    return request.accept_languages.best_match(['en', 'es'])

def create_app(config_overrides=None):
    app = Flask(__name__, static_folder='static', static_url_path='')
    
    # Configurar Base de Datos (Docker Postgres puerto 4950 por defecto)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 
        'postgresql+psycopg://user:password@localhost:4950/products_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configurar Babel para internacionalización (i18n)
    app.config['BABEL_DEFAULT_LOCALE'] = 'es'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

    # Configurar JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key-123')

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    jwt.init_app(app)
    
    with app.app_context():
        from models import Product, Sale, User
        import routes
        app.register_blueprint(routes.api_bp)
        db.create_all()
        
        # Crear usuario por defecto si no existe
        if not User.query.filter_by(username='admin').first():
            default_user = User(username='admin')
            default_user.set_password('admin')
            db.session.add(default_user)
            db.session.commit()

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.route('/login')
    def login_page():
        return app.send_static_file('login.html')

    @app.route('/register')
    def register_page():
        return app.send_static_file('register.html')

    return app

