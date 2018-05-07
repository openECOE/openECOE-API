import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required
from flask_principal import Principal
from flask_potion import Api

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
principals = Principal()
api_app = Api()


def create_app():
    app_settings = os.getenv(
        'APP_SETTINGS',
        'config.DevelopmentConfig'
    )

    app = Flask(__name__)
    app.config.from_object(app_settings)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    principals.init_app(app)

    if app.config.get('API_AUTH'):
        api_app.decorators.append(login_required)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
