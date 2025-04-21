from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .forms import RegistrationForm, LoginForm
from app.services.user_service import UserService
from app.tasks.email_tasks import send_welcome_email
from . import auth_bp


@auth_bp.route('/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = UserService.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            login_user(user)
            flash('Registration successful! Welcome!', 'success')
            # Trigger Celery task for welcome email
            send_welcome_email.delay(user.email)
            return redirect(url_for('auth.profile'))
        except Exception as e:
            flash(f'Error during registration: {str(e)}', 'danger')

    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = UserService.get_user_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)


@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
