from unittest.mock import patch

import pytest

from app import create_app
from app import db as _db
from app.config import Config


@pytest.fixture(scope="function")
def app():
    Config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    app = create_app()

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def mock_redis():
    with patch("app.utils.auth.redis_client") as mock_redis_client:
        yield mock_redis_client


@pytest.fixture(scope="function")
def db(app):
    yield _db
    _db.session.rollback()
    _db.session.remove()
