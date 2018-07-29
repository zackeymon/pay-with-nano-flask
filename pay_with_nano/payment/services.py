from copy import deepcopy
from time import sleep

from flask import render_template, redirect, url_for
from flask_login import current_user

from pay_with_nano.config import MASTER_WALLET_ID
from pay_with_nano.core import rpc_services, live_price_services
from pay_with_nano.core.models import Transaction
from pay_with_nano.database import db
from pay_with_nano.payment.forms import PaymentForm

unsettled_payment_sessions = {}


def payment_info_complete(arguments):
    return 'address' in arguments and 'amount' in arguments


def render_handle_payment_page(arguments):
    address = arguments['address']
    amount = arguments['amount']
    currency = dict(Transaction.SUPPORTED_CURRENCIES)[arguments['currency']]
    amount_nano = amount if currency == 'NANO' else convert_to_nano(currency, amount)
    uri = rpc_services.generate_uri(address, amount_nano)

    return render_template('handle_payment.html', amount=amount, amount_nano=amount_nano,
                           address=address, uri=uri, currency=currency)


def render_payment_request_page(arguments):
    form = PaymentForm(csrf_enabled=False)
    live_price_dict = live_price_services.get_nano_live_prices()

    if 'address' in arguments:
        form.address.data = arguments['address']

    return render_template('create_payment.html', form=form, live_price_dict=live_price_dict)


def begin_payment_session(user, currency, amount):
    transition_address = rpc_services.payment_begin(MASTER_WALLET_ID)
    unsettled_payment_sessions[transition_address] = dict(user=deepcopy(user), currency=currency, amount=str(amount))
    return transition_address


def settle_payment(transaction_dict):
    transaction = Transaction(**transaction_dict)
    transition_address = transaction.destination

    if transition_address in unsettled_payment_sessions:
        # A merchant payment
        additional_transaction_info = unsettled_payment_sessions.pop(transition_address)
        receiving_user = additional_transaction_info['user']

        if transaction.status == 'success':
            print("transfer fund in 40 seconds...")
            sleep(40)
            # Send fund to receiving address
            print(rpc_services.send_nano(
                wallet_id=MASTER_WALLET_ID,
                source=transition_address,
                destination=receiving_user.receiving_address,
                amount_nano=transaction.amount_nano
            ))

        transaction.user_id = receiving_user.id
        transaction.currency = additional_transaction_info['currency']
        transaction.amount = additional_transaction_info['amount']

        db.session.add(transaction)
        db.session.commit()


def convert_to_nano(currency, amount):
    live_price_dict = live_price_services.get_nano_live_prices()
    amount_nano_precise = float(amount) / live_price_dict[currency]

    return '{0:.3g}'.format(amount_nano_precise)


def serve_payment_page(currency, amount):
    transition_address = begin_payment_session(current_user, currency, amount)
    return redirect(url_for('.payment_page', address=transition_address, amount=amount, currency=currency))