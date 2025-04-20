print("Loading celery.py")
from celery import Celery
from flask import Flask

celery = Celery()

def init_celery(app: Flask) -> Celery:
    print("Initializing Celery")
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        accept_content=['json'],
        task_serializer='json',
        result_serializer='json',
        timezone='UTC'
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery