from datetime import datetime
from time import sleep

import nano

from terminal.models import User
from .rpc_client import RPCClient
from database import db

TOTAL_WAIT_TIME = 18
POLLING_INTERVAL = 2


# Unit conversions
def raw_to_nano(raw_amount):
    return nano.conversion.convert(raw_amount, from_unit="raw", to_unit="Mrai")


def nano_to_raw(nano_amount):
    return nano.conversion.convert(nano_amount, from_unit="Mrai", to_unit="raw")


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
    rpc = RPCClient()
    pending_blocks = rpc.get_account_pending_blocks(to_address)

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


def generate_uri(address, required_amount):
    required_raw_amount = nano_to_raw(required_amount)
    return "xrb:{address}?amount={raw_amount}".format(address=address, raw_amount=required_raw_amount)


def get_wallet_id(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.wallet_id
    return None


def validated(username, password):
    rpc = RPCClient()

    wallet_id = get_wallet_id(username)

    print(wallet_id)

    if wallet_id is None or not rpc.unlock_wallet(wallet_id, password):
        # username not found / password wrong
        return False

    return True


def initialise_user(username, password):
    rpc = RPCClient()

    # make new wallet
    wallet_id = rpc.create_new_wallet()

    # change password
    rpc.change_wallet_password(wallet_id, password)

    # lock wallet
    rpc.lock_wallet(wallet_id)

    # save user to database
    new_user = User(username=username, wallet_id=wallet_id)
    db.session.add(new_user)
    db.session.commit()
