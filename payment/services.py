from time import sleep

from flask import render_template
from api.services import generate_uri, nano_to_raw
from database import db
from models import Transaction
from payment.forms import PaymentForm
from nano import RPCClient
from copy import deepcopy

MASTER_WALLET_ID = '39A86A90379995AD2B9C539A24A28ECD889DCCAF29C4A2B43EB4EF483B71B50A'

unsettled_payment_sessions = {}
rpc = RPCClient()


def payment_info_complete(arguments):
    return 'address' in arguments and 'amount' in arguments


def render_handle_payment_page(arguments):
    address = arguments['address']
    amount = arguments['amount']
    uri = generate_uri(address, amount)
    return render_template('handle_payment.html', amount=amount, address=address, uri=uri)


def render_payment_request_page(arguments):
    form = PaymentForm(csrf_enabled=False)
    if 'address' in arguments:
        form.address.data = arguments['address']

    return render_template('create_payment.html', form=form)


def begin_payment_session(user):
    transition_address = rpc.payment_begin(MASTER_WALLET_ID)
    unsettled_payment_sessions[transition_address] = deepcopy(user)
    return transition_address


def settle_payment(transaction_dict):
    transaction = Transaction(**transaction_dict)
    transition_address = transaction.to_address
    if transition_address in unsettled_payment_sessions:
        receiving_user = unsettled_payment_sessions.pop(transition_address)
        transaction.user_id = receiving_user.id
        db.session.add(transaction)
        db.session.commit()

        if transaction.success:
            print("transfer fund in 10 seconds...")
            sleep(10)
            # Send fund to receiving address
            print(rpc.send(
                wallet=MASTER_WALLET_ID,
                source=transition_address,
                destination=receiving_user.receiving_address,
                amount=int(nano_to_raw(transaction.amount)),
                id=str(transaction.id)
            ))


