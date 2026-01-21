from flask import Flask
from flask_cors import CORS

from app.extensions import db


def create_app(config_object="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    CORS(app)
    db.init_app(app)
    from app import models  # noqa: F401

    return app
