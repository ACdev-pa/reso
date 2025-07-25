from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from .routes import frontend, backend
    app.register_blueprint(frontend.bp)
    app.register_blueprint(backend.bp)

    return app
