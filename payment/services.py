from flask import render_template
from api.services import generate_uri
from payment.forms import PaymentForm


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
