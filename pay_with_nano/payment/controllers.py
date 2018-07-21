import os
from pay_with_nano import basedir
from flask import Blueprint, request, redirect, url_for
from pay_with_nano.payment.services import payment_info_complete, render_handle_payment_page, render_payment_request_page, \
    begin_payment_session, settle_payment
from flask_login import current_user, login_required

pay = Blueprint('pay', __name__, template_folder=os.path.join(basedir, 'templates', 'payment'))


@pay.route('/')
def payment_page():
    if payment_info_complete(request.args):
        return render_handle_payment_page(request.args)
    else:
        return render_payment_request_page(request.args)


@pay.route('/start_payment', methods=['POST'])
@login_required
def start_payment():
    transition_address = begin_payment_session(current_user)
    return redirect(url_for('.payment_page', address=transition_address, amount=request.form['amount']))


@pay.route('/finish_payment', methods=['POST'])
def finish_payment():
    settle_payment(request.get_json())
    return 'yeah boi'
