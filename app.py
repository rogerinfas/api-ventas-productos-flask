from flask import Flask, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

db = SQLAlchemy()
babel = Babel()

def get_locale():
    # If a user is logged in, you may want to return their locale
    return request.accept_languages.best_match(['en', 'es'])

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    
    # Configure Database (Docker Postgres port 4950)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://user:password@localhost:4950/products_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure Babel for i18n
    app.config['BABEL_DEFAULT_LOCALE'] = 'es'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

    db.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    
    with app.app_context():
        from models import Product, Sale
        import routes
        app.register_blueprint(routes.api_bp)
        db.create_all()

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001, host='0.0.0.0')
