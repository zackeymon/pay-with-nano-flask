from .models import Transaction
import requests

API_ROOT = 'https://min-api.cryptocompare.com/data/'


def get_nano_live_prices():
    # TODO: refactor here
    endpoint = 'price'
    currency_string = ','.join(dict(Transaction.SUPPORTED_CURRENCIES).values())
    payload = {'fsym': 'NANO', 'tsyms': currency_string}

    r = requests.get(API_ROOT + endpoint, params=payload)
    return r.json()
