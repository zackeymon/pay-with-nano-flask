import os

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from pay_with_nano import basedir
from pay_with_nano.core import rpc_services
from pay_with_nano.core.models import User
from pay_with_nano.core.rpc_services import get_balance_nano
from pay_with_nano.terminal.services import validated, initialise_user, change_receiving_address, get_user_transactions, \
    get_transaction_from_id, can_refund, refund
from .forms import LoginForm, RegisterForm, ChangeAddressForm, RequestAmountForm

terminal = Blueprint('terminal', __name__, template_folder=os.path.join(basedir, 'templates', 'terminal'))

login_manager = LoginManager()


@terminal.record_once
def on_load(state):
    login_manager.init_app(state.app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@terminal.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('.dashboard'))
    return redirect(url_for('.login_page'))


@terminal.route('/login', methods=['GET', 'POST'])
def login_page():
    login_form = LoginForm(request.form)

    # POST
    if login_form.validate_on_submit():
        if validated(username=login_form.username.data, password=login_form.password.data):
            this_user = User.query.filter_by(username=login_form.username.data).first()
            login_user(this_user)
            return redirect(url_for('.dashboard'))
        # 2nd validation failed
        flash('Wrong username or password!')

    # GET, form includes errors
    return render_template('terminal/login.html', login_form=login_form)


@terminal.route('/register', methods=['GET', 'POST'])
def registration_page():
    register_form = RegisterForm(request.form)

    # POST
    if register_form.validate_on_submit():
        # TODO: try-catch this
        initialise_user(username=register_form.username.data, password=register_form.password.data, email=register_form.email.data)
        flash("Registration success! Please log in.")
        return redirect(url_for('.login_page'))

    # GET, form includes errors
    return render_template('register.html', register_form=register_form)


@terminal.route('/dashboard')
@login_required
def dashboard():
    if current_user.receiving_address is None:
        flash('Please set a receiving address before continue')
        return redirect(url_for('.change_address'))

    form = RequestAmountForm()
    transactions = get_user_transactions(current_user)
    refund_address_balance = get_balance_nano(current_user.refund_address)
    return render_template('dashboard.html', current_user=current_user, form=form, transactions=transactions,
                           refund_address_balance=refund_address_balance)


@terminal.route('/logout')
@login_required
def logout():
    rpc_services.lock_wallet(current_user.wallet_id)
    logout_user()
    flash('Successfully logged out!')
    return redirect(url_for('.login_page'))


@terminal.route('/debug')
def debug():
    return current_user.username + current_user.wallet_id


@terminal.route('/change_address', methods=['GET', 'POST'])
@login_required
def change_address():
    form = ChangeAddressForm(request.form)

    # POST
    if form.validate_on_submit():
        if validated(current_user.username, form.password.data):
            change_receiving_address(current_user, form.new_address.data)
            flash('Address updated!', 'success')
        else:
            flash('Wrong password! Address unchanged.', 'error')

        return redirect(url_for('.change_address'))

    # GET, form includes errors
    return render_template('change_address.html', form=form, current_user=current_user)


@terminal.route('/start_refund')
@login_required
def start_refund():
    transaction = get_transaction_from_id(request.args['transaction_id'])
    if can_refund(current_user, transaction):
        # TODO: receive blocks
        block_hash = refund(current_user, transaction)
        print(block_hash)
        if block_hash:
            return 'Refunded'
        return 'Unknown Error'
    return 'Not authorised or not enough fund!'
