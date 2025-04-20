import os
from .base import BaseConfig

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # Inherit SQLALCHEMY_DATABASE_URI from BaseConfig
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')