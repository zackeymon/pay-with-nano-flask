import requests
from flask import Blueprint, request, jsonify

from . import services

api = Blueprint('api', __name__)


@api.route('/')
def default():
    return 'API is working!'


@api.route('/payment_received')
def payment_received():
    address = request.args['address']
    amount = request.args['amount']

    transaction = services.make_transaction_response(address, amount)

    # TODO: change to task queue
    try:
        requests.post("http://localhost:5000/api/process_blocks", json=transaction)
    except requests.exceptions.ReadTimeout:
        pass

    return jsonify(transaction)


@api.route('/process_blocks', methods=['POST'])
def process_blocks():
    # process the pending blocks in the background
    try:
        requests.post('http://localhost:5000/pay/finish_payment', json=request.get_json(), timeout=0.0001)
    except requests.exceptions.RequestException:
        pass

    return 'success'


@api.route('/callback', methods=['POST'])
def callback():
    print(request.get_data())
    return 'thanks'
