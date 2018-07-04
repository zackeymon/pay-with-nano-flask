from flask import Blueprint, request, render_template

pay = Blueprint('pay', __name__, static_folder='static', template_folder='templates')


@pay.route('/')
def payment_page():
    return render_template('create_payment.html')