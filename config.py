import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql+psycopg://user:password@localhost:4950/products_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = 'es'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key-123')
