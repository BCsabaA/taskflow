from __future__ import annotations
import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db_path = os.path.join(app.instance_path, "taskflow.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        from .models import User
        db.create_all()

    return app