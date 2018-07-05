from flask import Blueprint, request, render_template
from api.services import generate_uri

pay = Blueprint('pay', __name__, static_folder='static', template_folder='templates')


@pay.route('/')
def payment_page():
    if 'amount' not in request.args:
        return render_template('create_payment.html')

    amount = request.args.get('amount')
    address = request.args.get('address')
    uri = generate_uri(address, amount)

    return render_template('handle_payment.html', amount=amount, address=address, uri=uri)
