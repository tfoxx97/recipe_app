from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from recipe_app.config import Config

db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()
jwt = JWTManager()
swagger_ui_blueprint = get_swaggerui_blueprint(
    Config.SWAGGER_URL,
    Config.API_URL,
    config={
        'app_name': 'Recipe API'
    }
)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ckeditor.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    from recipe_app.routes import recipe_routes
    app.register_blueprint(recipe_routes)
    app.register_blueprint(swagger_ui_blueprint, url_prefix=Config.SWAGGER_URL)

    return app

app = create_app()