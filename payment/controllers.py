from flask import Blueprint, request
from payment.services import payment_info_complete, render_handle_payment_page, render_payment_request_page

pay = Blueprint('pay', __name__, static_folder='static', template_folder='templates')


@pay.route('/')
def payment_page():
    if payment_info_complete(request.args):
        return render_handle_payment_page(request.args)
    else:
        return render_payment_request_page(request.args)




