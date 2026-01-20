import pytest
from sqlalchemy.pool import StaticPool

from app import create_app
from app.extensions import db


@pytest.fixture()
def app():
    app = create_app("config.TestingConfig")
    app.config.update(
        SQLALCHEMY_ENGINE_OPTIONS={
            "connect_args": {"check_same_thread": False},
            "poolclass": StaticPool,
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture()
def session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()
