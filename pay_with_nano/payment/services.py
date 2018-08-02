from copy import deepcopy

from flask import render_template

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
    payment_form = PaymentForm(csrf_enabled=False)
    live_price_dict = live_price_services.get_nano_live_prices()

    if 'address' in arguments:
        payment_form.address.data = arguments['address']

    return render_template('create_payment.html', payment_form=payment_form, live_price_dict=live_price_dict)


def begin_payment_session(user, currency, amount):
    transition_address = rpc_services.payment_begin(user.transition_wallet_id)
    unsettled_payment_sessions[transition_address] = dict(user=deepcopy(user), currency=currency, amount=str(amount))
    return transition_address


def settle_payment(transaction_dict):
    transaction = Transaction(**transaction_dict)
    transition_address = transaction.destination

    if transition_address in unsettled_payment_sessions:
        # A merchant payment
        additional_transaction_info = unsettled_payment_sessions.pop(transition_address)
        receiving_user = additional_transaction_info['user']

        # Populate model
        transaction.user_id = receiving_user.id
        transaction.currency = additional_transaction_info['currency']
        transaction.amount = additional_transaction_info['amount']

        # Save to database
        db.session.add(transaction)
        db.session.commit()

        if transaction.status == 'success':
            print("Waiting for receive block")
            if rpc_services.payment_wait(transition_address, transaction.amount_nano, 80000):
                print("Sending fund to receiving address...")
                print(rpc_services.send_nano(
                    wallet_id=receiving_user.transition_wallet_id,
                    source=transition_address,
                    destination=receiving_user.receiving_address,
                    amount_nano=transaction.amount_nano,
                    id=transition_address
                ))
            else:
                raise TimeoutError


def convert_to_nano(currency, amount):
    live_price_dict = live_price_services.get_nano_live_prices()
    amount_nano_precise = float(amount) / live_price_dict[currency]

    return '{0:.3g}'.format(amount_nano_precise)
