Run migrations:
Initialize Flask-Migrate: flask db init (if not already done).
Generate migration for the User model: flask db migrate -m "Add User model".
Apply migrations: flask db upgrade.