import os
from pay_with_nano import basedir
from flask import Blueprint, request, redirect, url_for, render_template, flash

from pay_with_nano.payment.forms import MerchantRequestForm
from pay_with_nano.payment.services import payment_info_complete, render_handle_payment_page, \
    render_payment_request_page, \
    begin_payment_session, settle_payment, convert_to_nano
from flask_login import current_user, login_required

pay = Blueprint('pay', __name__, template_folder=os.path.join(basedir, 'templates', 'payment'))


@pay.route('/')
def payment_page():
    if payment_info_complete(request.args):
        return render_handle_payment_page(request.args)
    else:
        return render_payment_request_page(request.args)


@pay.route('/merchant', methods=['GET', 'POST'])
@login_required
def merchant_payment_page():
    merchant_request_form = MerchantRequestForm()

    if merchant_request_form.validate_on_submit():
        currency = merchant_request_form.currency.data
        amount = merchant_request_form.amount.data

        if merchant_request_form.pin.data == current_user.pin:
            transition_address = begin_payment_session(current_user, currency, amount)
            amount_nano = convert_to_nano(currency, amount)

            return redirect(url_for('.payment_page', address=transition_address, amount=amount_nano))
        flash('PIN incorrect!', 'error')
    return render_template('payment/merchant_pos.html', merchant_request_form=merchant_request_form)


@pay.route('/finish_payment', methods=['POST'])
def finish_payment():
    settle_payment(request.get_json())
    return 'yeah boi'
