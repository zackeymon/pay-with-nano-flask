import nano

from time import sleep
from datetime import datetime

from django.core import serializers

from .rpc_client import RPCClient

TOTAL_WAIT_TIME = 60
POLLING_INTERVAL = 3


def required_amount_received(address, required_amount):
    # 60/3 = 20 times
    polls = int(TOTAL_WAIT_TIME / POLLING_INTERVAL)

    rpc = RPCClient()
    prev_balance, cur_balance = None, None

    for i in range(polls):
        print("Polling...")
        cur_balance = rpc.check_account_total_balance(address)
        if cur_balance != prev_balance and prev_balance is not None:
            print("ACCOUNT BALANCE CHANGED!")
            actual_amount = cur_balance - prev_balance

            if actual_amount == required_amount:
                return True

        prev_balance = cur_balance

        sleep(POLLING_INTERVAL)

    # Timeout
    return False


def find_from_address(to_address, sent_amount):
    return 'xrb_todo'


def generate_transaction_model(address, required_amount):
    transaction = dict(success=False)

    if required_amount_received(address, required_amount):
        transaction['success'] = True
        transaction['from_address'] = find_from_address(address, required_amount)
        transaction['timestamp'] = datetime.utcnow()

    return transaction


def raw_to_nano(raw_amount):
    return nano.conversion.convert(raw_amount, from_unit="raw", to_unit="Mrai")


def nano_to_raw(nano_amount):
    return nano.conversion.convert(nano_amount, from_unit="Mrai", to_unit="raw")
