import nano


class RPCClient:
    def __init__(self, host_url="http://localhost", port="7076"):
        self.client = nano.rpc.Client(host="{0}:{1}".format(host_url, port), session=None)

    def check_account_total_balance(self, address):
        body = self.client.account_balance(account=address)
        return body["balance"] + body["pending"]

    def get_account_pending_blocks(self, address):
        hashes = self.client.accounts_pending([address])[address]
        if hashes:
            print("yes!")
            return self.client.blocks_info(hashes)
        print("no")
        return {}

    def unlock_wallet(self, wallet_id, password):
        return self.client.wallet_unlock(wallet_id, password)

    def lock_wallet(self, wallet_id):
        return self.client.wallet_lock(wallet_id)