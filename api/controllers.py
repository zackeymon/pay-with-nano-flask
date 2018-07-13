from flask import Blueprint, request, jsonify
from . import services

api = Blueprint('api', __name__)


@api.route('/')
def default():
    return 'api is workinggg!'


@api.route('/payment_received')
def payment_received():
    address = request.args.get('address')
    amount = request.args.get('amount')

    return jsonify(services.make_transaction_response(address, amount))