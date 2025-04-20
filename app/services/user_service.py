from app.models.user import User
from app.extensions.database import db
from app.tasks.email_tasks import send_welcome_email


class UserService:
    @staticmethod
    def create_user(username, email, password):
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            raise ValueError("Username or email already exists")

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Trigger Celery task to send welcome email
        send_welcome_email.delay(user.email, user.username)

        return user

    @staticmethod
    def authenticate(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None