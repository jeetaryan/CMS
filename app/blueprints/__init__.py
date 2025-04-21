from flask import Flask
from .auth import auth_bp


def auth_blueprints(app: Flask):
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(auth_bp, url_prefix='/auth')
