import nano


class RPCClient:
    def __init__(self, host_url="http://localhost", port="7076"):
        self.rpc = nano.rpc.Client(host="{0}:{1}".format(host_url, port), session=None)

    def check_account_total_balance(self, address):
        body = self.rpc.account_balance(account=address)
        return body["balance"] + body["pending"]

    def get_account_pending_blocks(self, address):
        hashes = self.rpc.accounts_pending([address])[address]
        if hashes:
            print("yes!")
            return self.rpc.blocks_info(hashes)
        print("no")
        return {}

