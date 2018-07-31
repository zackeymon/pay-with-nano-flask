import os
from functools import wraps

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from pay_with_nano import basedir
from pay_with_nano.core import rpc_services
from pay_with_nano.core.models import User
from pay_with_nano.core.rpc_services import get_balance_nano
from pay_with_nano.terminal.services import validated, initialise_user, change_receiving_address, get_user_transactions, \
    get_transaction_from_id, can_refund, refund, change_pin, generate_seed
from .forms import LoginForm, RegisterForm, ChangeAddressForm, ChangePinForm, RefundForm

terminal = Blueprint('terminal', __name__, template_folder=os.path.join(basedir, 'templates', 'terminal'))

login_manager = LoginManager()


@terminal.record_once
def on_load(state):
    login_manager.init_app(state.app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def full_info_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.pin is None or current_user.receiving_address is None:
            return redirect(url_for('.settings'))
        return func(*args, **kwargs)

    return decorated_view


@terminal.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('.dashboard'))
    return redirect(url_for('.login_page'))


@terminal.route('/register', methods=['GET', 'POST'])
def registration_page():
    register_form = RegisterForm(request.form)

    # POST
    if register_form.validate_on_submit():
        # TODO: try-catch this
        initialise_user(username=register_form.username.data, password=register_form.password.data,
                        email=register_form.email.data)
        flash('Registration success! Please log in.', 'success')
        return redirect(url_for('.login_page'))

    # GET, form includes errors
    return render_template('terminal/register.html', register_form=register_form)


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
        flash('Wrong username or password!', 'error')

    # GET, form includes errors
    return render_template('terminal/login.html', login_form=login_form)


@terminal.route('/logout')
@login_required
def logout():
    rpc_services.lock_wallet(current_user.wallet_id)
    logout_user()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('.login_page'))


@terminal.route('/dashboard')
@login_required
@full_info_required
def dashboard():
    receiving_address_balance = get_balance_nano(current_user.receiving_address)
    refund_address_balance = get_balance_nano(current_user.refund_address)
    return render_template('terminal/dashboard.html', current_user=current_user,
                           refund_address_balance=refund_address_balance,
                           receiving_address_balance=receiving_address_balance,
                           seed=generate_seed(current_user))


@terminal.route('/history')
@login_required
@full_info_required
def transaction_history():
    transactions = get_user_transactions(current_user)
    return render_template('terminal/transaction_history.html',
                           transactions=transactions, seed=generate_seed(current_user))


@terminal.route('/launch_pos')
@login_required
@full_info_required
def launch_pos():
    return redirect(url_for('pay.merchant_payment_page'))


@terminal.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    change_address_form = ChangeAddressForm()
    change_pin_form = ChangePinForm()

    # change_address_form logic
    if 'address_submit' in request.form and change_address_form.validate():
        if validated(current_user.username, change_address_form.password.data):
            change_receiving_address(current_user, change_address_form.new_address.data)
            flash('Address updated!', 'success')
        else:
            flash('Wrong password! Address unchanged.', 'error')

        return redirect(url_for('.settings'))

    # change_pin_form logic
    if 'pin_submit' in request.form and change_pin_form.validate():
        if validated(current_user.username, change_pin_form.password.data):
            change_pin(current_user, str(change_pin_form.pin.data))
            flash('PIN set!', 'success')
        else:
            flash('Wrong password! PIN unchanged.', 'error')

        return redirect(url_for('.settings'))

    if current_user.receiving_address is None:
        flash('Please specify a receiving address before continue.', 'warning')
    if current_user.pin is None:
        flash('Please set a PIN before continue.', 'warning')

    # form includes validation errors
    return render_template('terminal/settings.html', change_address_form=change_address_form,
                           change_pin_form=change_pin_form, current_user=current_user, seed=generate_seed(current_user))


@terminal.route('/confirm_refund', methods=['GET', 'POST'])
@login_required
@full_info_required
def confirm_refund():
    refund_form = RefundForm()
    transaction = get_transaction_from_id(request.args['transaction_id'])

    if refund_form.validate_on_submit():
        if validated(current_user.username, refund_form.password.data):
            # TODO: receive blocks
            block_hash = refund(current_user, refund_form.password.data, transaction)
            if block_hash:
                return render_template('terminal/refund_complete.html', block_hash=block_hash)
            flash('Unknown Error :o', 'error')
        else:
            flash('Wrong password!', 'error')
    if can_refund(current_user, transaction):
        return render_template('terminal/refund_confirmation.html', refund_form=refund_form, transaction=transaction)

    flash('You cannot refund this transaction. Insufficient fund or not authorised.', 'error')
    return redirect(url_for('.transaction_history'))


@terminal.route('/debug')
def debug():
    return render_template('test.html', seed=current_user.wallet_id)
