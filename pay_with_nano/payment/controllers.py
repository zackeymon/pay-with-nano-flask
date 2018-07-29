import os
from pay_with_nano import basedir
from flask import Blueprint, request, render_template, flash

from pay_with_nano.core import live_price_services
from pay_with_nano.payment.forms import MerchantRequestForm
from pay_with_nano.payment.services import payment_info_complete, render_handle_payment_page, \
    render_payment_request_page, \
    settle_payment, serve_payment_page
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
        if merchant_request_form.pin.data == current_user.pin:
            return serve_payment_page(currency=merchant_request_form.currency.data,
                                      amount=merchant_request_form.amount.data)
        flash('PIN incorrect!', 'error')

    live_price_dict = live_price_services.get_nano_live_prices()
    return render_template('payment/merchant_pos.html', merchant_request_form=merchant_request_form,
                           live_price_dict=live_price_dict)


@pay.route('/finish_payment', methods=['POST'])
def finish_payment():
    settle_payment(request.get_json())
    return 'yeah boi'
