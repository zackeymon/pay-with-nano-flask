from time import sleep
from flask import render_template
import uuid

from pay_with_nano.config import MASTER_WALLET_ID
from pay_with_nano.core import rpc_services
from pay_with_nano.database import db
from pay_with_nano.core.models import Transaction
from pay_with_nano.payment.forms import PaymentForm
from copy import deepcopy

unsettled_payment_sessions = {}


def payment_info_complete(arguments):
    return 'address' in arguments and 'amount' in arguments


def render_handle_payment_page(arguments):
    address = arguments['address']
    amount = arguments['amount']
    uri = rpc_services.generate_uri(address, amount)
    return render_template('handle_payment.html', amount=amount, address=address, uri=uri)


def render_payment_request_page(arguments):
    form = PaymentForm(csrf_enabled=False)
    if 'address' in arguments:
        form.address.data = arguments['address']

    return render_template('create_payment.html', form=form)


def begin_payment_session(user):
    transition_address = rpc_services.payment_begin(MASTER_WALLET_ID)
    unsettled_payment_sessions[transition_address] = deepcopy(user)
    return transition_address


def settle_payment(transaction_dict):
    transaction = Transaction(**transaction_dict)
    transition_address = transaction.to_address
    if transition_address in unsettled_payment_sessions:
        receiving_user = unsettled_payment_sessions.pop(transition_address)
        transaction.user_id = receiving_user.id

        if transaction.success:
            print("transfer fund in 30 seconds...")
            sleep(30)
            # Send fund to receiving address
            print(rpc_services.send_nano(
                wallet_id=MASTER_WALLET_ID,
                source=transition_address,
                destination=receiving_user.receiving_address,
                amount_nano=transaction.amount
            ))

        db.session.add(transaction)
        db.session.commit()


