import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_BLACKLIST_ENABLED = True
    CKEDITOR_HEIGHT = 500
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_CODE_THEME = 'mono-blue'
    SWAGGER_URL = "/docs"
    API_URL = "/static/recipe_docs.json"