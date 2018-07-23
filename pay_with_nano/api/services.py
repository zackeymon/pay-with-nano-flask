from datetime import datetime
from time import sleep

from pay_with_nano.config import TOTAL_WAIT_TIME, POLLING_INTERVAL
from pay_with_nano.core import rpc_services
from pay_with_nano.core.rpc_services import nano_to_raw
from .rpc_client import RPCClient


# Receive payment
def required_amount_received(address, required_amount):
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


def get_hash_and_sender(to_address, sent_raw_amount):
    pending_blocks = rpc_services.get_pending_blocks_for_address(to_address)

    for block_hash, block in pending_blocks.items():
        if block['amount'] == sent_raw_amount:
            return block_hash, block['block_account']

    # TODO: check account chain or manually accept block?
    raise NotImplementedError


def make_transaction_response(address, required_amount):
    transaction = dict(success=False, amount=required_amount, to_address=address)
    required_raw_amount = nano_to_raw(required_amount)

    if required_amount_received(address, required_raw_amount):
        transaction['success'] = True
        transaction['hash'], transaction['from_address'] = get_hash_and_sender(address, required_raw_amount)

    transaction['timestamp'] = str(datetime.utcnow())
    return transaction



