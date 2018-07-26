from nano import RPCClient, conversion
import uuid

_rpc_client = RPCClient()


# Unit conversions
def raw_to_nano(raw_amount):
    return conversion.convert(raw_amount, from_unit="raw", to_unit="Mrai")


def nano_to_raw(nano_amount):
    return conversion.convert(nano_amount, from_unit="Mrai", to_unit="raw")


# Generate URI
def generate_uri(address, required_nano_amount):
    required_raw_amount = nano_to_raw(required_nano_amount)
    return "xrb:{address}?amount={raw_amount}".format(address=address, raw_amount=required_raw_amount)


# Query database/ledger
def get_balance_nano(address):
    body = _rpc_client.account_balance(account=address)
    return raw_to_nano(body["balance"] + body["pending"])


def get_pending_blocks_for_address(address):
    pending_block_hashes = _rpc_client.accounts_pending([address])[address]
    return _rpc_client.blocks_info(pending_block_hashes)


# Wallet operations
def create_new_wallet():
    return _rpc_client.wallet_create()


def create_new_account(wallet_id):
    return _rpc_client.account_create(wallet_id)


def unlock_wallet(wallet_id, password):
    return _rpc_client.wallet_unlock(wallet_id, password)


def lock_wallet(wallet_id):
    return _rpc_client.wallet_lock(wallet_id)


def change_wallet_password(wallet_id, password):
    return _rpc_client.password_change(wallet_id, password)


# Send fund
def send_nano(wallet_id, source, destination, amount_nano):
    return _rpc_client.send(
        wallet=wallet_id,
        source=source,
        destination=destination,
        amount=int(nano_to_raw(amount_nano)),
        id=str(uuid.uuid4())
    )


def payment_begin(wallet_id):
    return _rpc_client.payment_begin(wallet_id)

