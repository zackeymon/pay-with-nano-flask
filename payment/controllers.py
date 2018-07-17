from flask import Blueprint, request, render_template
from api.services import generate_uri
from .forms import PaymentForm

pay = Blueprint('pay', __name__, static_folder='static', template_folder='templates')


@pay.route('/')
def payment_page():
    # getting paid
    if 'address' in request.args and 'amount' in request.args:
        amount = request.args.get('amount')
        address = request.args.get('address')
        uri = generate_uri(address, amount)
        return render_template('handle_payment.html', amount=amount, address=address, uri=uri)

    # making pay request
    form = PaymentForm()
    if 'address' in request.args:
        form.address.data = request.args.get('address')

    return render_template('create_payment.html', form=form)



