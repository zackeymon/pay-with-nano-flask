from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from api.services import validated, initialise_user
from api.models import User
from .forms import LoginForm, RegisterForm

terminal = Blueprint('terminal', __name__, static_folder='static', template_folder='templates')

login_manager = LoginManager()


@terminal.record_once
def on_load(state):
    login_manager.init_app(state.app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@terminal.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm(request.form)

    # POST
    if form.validate_on_submit():
        if validated(username=form.username.data, password=form.password.data):
            this_user = User.query.filter_by(username=form.username.data).first()
            login_user(this_user)
            return redirect(url_for('.dashboard'))
        # 2nd validation failed
        flash('Wrong username or password!')

    # GET, form includes errors
    return render_template('login.html', form=form)


@terminal.route('/register', methods=['GET', 'POST'])
def registration_page():
    form = RegisterForm(request.form)

    # POST
    if form.validate_on_submit():
        # TODO: try-catch this
        initialise_user(username=form.username.data, password=form.password.data)
        flash("Registration success! Please log in.")
        return redirect(url_for('.login_page'))

    # GET, form includes errors
    return render_template('register.html', form=form)


@terminal.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', current_user=current_user)


@terminal.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out!')
    return redirect(url_for('.login_page'))


@terminal.route('/debug')
def debug():
    return current_user.username + current_user.wallet_id
