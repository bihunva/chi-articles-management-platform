from flask import Flask

from app.config import Config
from app.extensions import db, migrate, jwt, bcrypt, api, redis_client
from app.views.article import article_bp
from app.views.auth import auth_bp
from app.views.user import user_bp


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    redis_client.init_app(app)


def register_blueprints(app: Flask) -> None:
    api.init_app(app)
    api.register_blueprint(auth_bp)
    api.register_blueprint(user_bp)
    api.register_blueprint(article_bp)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_blueprints(app)

    return app
