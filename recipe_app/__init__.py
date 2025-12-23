import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fbca68591a794800afa9f9433ccc598d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '1d6699be966f49e6b501219923eee798'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ckeditor = CKEditor(app)
jwt = JWTManager(app)
CKEDITOR_HEIGHT = 500
CKEDITOR_ENABLE_CODESNIPPET = True
CKEDITOR_CODE_THEME = 'mono-blue'
SWAGGER_URL = "/docs"
API_URL = "/static/recipe_docs.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Recipe API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

import recipe_app.routes