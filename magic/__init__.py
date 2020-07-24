import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from magic.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    # db.init_app(app)

    return app, db


app, db = create_app()
import magic.route
