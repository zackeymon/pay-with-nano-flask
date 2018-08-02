import os

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from pay_with_nano import basedir
from pay_with_nano.core import live_price_services
from pay_with_nano.payment.forms import MerchantRequestForm
from pay_with_nano.payment.services import payment_info_complete, render_handle_payment_page, \
    render_payment_request_page, \
    settle_payment, begin_payment_session

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
        if merchant_request_form.pin.data == current_user.pin:
            currency = merchant_request_form.currency.data
            amount = merchant_request_form.amount.data
            transition_address = begin_payment_session(current_user, currency, amount)
            return redirect(url_for('.payment_page', address=transition_address, amount=amount, currency=currency))
        flash('PIN incorrect!', 'error')

    live_price_dict = live_price_services.get_nano_live_prices()
    return render_template('payment/merchant_pos.html', merchant_request_form=merchant_request_form,
                           live_price_dict=live_price_dict)


@pay.route('/finish_payment', methods=['POST'])
def finish_payment():
    settle_payment(request.get_json())
    return 'yeah boi'
