from flask import Blueprint, request, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from api.services import validated, initialise_user
from api.models import User

terminal = Blueprint('terminal', __name__, static_folder='static', template_folder='templates')

login_manager = LoginManager()


@terminal.record_once
def on_load(state):
    login_manager.init_app(state.app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@terminal.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')


@terminal.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')

    # POST
    if validated(username=request.form['username'], password=request.form['password']):
        this_user = User.query.filter_by(username=request.form['username'])[0]
        login_user(this_user)
        return 'Logged in!'
    else:
        return 'Wrong username or password!'


@terminal.route('/register', methods=['GET', 'POST'])
def registration_page():
    if request.method == 'GET':
        return render_template('register.html')

    # if validated
    initialise_user(username=request.form['username'], password=request.form['password'])
    return "Registration Success!"


@terminal.route('/debug')
def debug():
    return current_user.username + current_user.wallet_id
