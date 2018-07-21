from nano import RPCClient, conversion

_rpc_client = RPCClient()


# Unit conversions
def raw_to_nano(raw_amount):
    return conversion.convert(raw_amount, from_unit="raw", to_unit="Mrai")


def nano_to_raw(nano_amount):
    return conversion.convert(nano_amount, from_unit="Mrai", to_unit="raw")


# Query database/ledger
def get_pending_blocks_to_address(address):
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
