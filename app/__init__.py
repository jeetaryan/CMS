from flask import Flask
from .extensions.database import init_db
from .extensions.migration import init_migration
from .extensions.auth import init_auth
from .extensions.cache import init_cache
from .blueprints import auth_blueprints
from .extensions.celery import init_celery


def create_app(config_name='development'):
    app = Flask(__name__)

    # Load configuration
    from .config import config
    app.config.from_object(config[config_name])

    # Initialize extensions
    init_db(app)
    init_migration(app)
    init_auth(app)
    init_cache(app)

    # Register blueprints
    auth_blueprints(app)

    # Store celery in app for access
    init_celery(app)
    return app