from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
babel = Babel()
jwt = JWTManager()

def get_locale():
    return request.accept_languages.best_match(['en', 'es'])

def create_app(config_overrides=None):
    app = Flask(__name__, static_folder='../static', static_url_path='')
    app.config.from_object(Config)

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    jwt.init_app(app)

    with app.app_context():
        from app.models import user, product, sale
        from app.controllers import auth_controller, product_controller, sale_controller
        
        app.register_blueprint(auth_controller.auth_bp)
        app.register_blueprint(product_controller.product_bp)
        app.register_blueprint(sale_controller.sale_bp)
        
        db.create_all()
        
        # Crear usuario por defecto si no existe
        from app.models.user import User
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
