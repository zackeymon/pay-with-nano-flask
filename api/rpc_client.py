import nano


class RPCClient:
    def __init__(self, host_url="http://localhost", port="7076"):
        self.rpc = nano.rpc.Client(host="{0}:{1}".format(host_url, port), session=None)

    def check_account_total_balance(self, address):
        body = self.rpc.account_balance(account=address)
        return body["balance"] + body["pending"]

