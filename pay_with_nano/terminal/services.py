from decimal import Decimal
import hashlib
from pay_with_nano.core import rpc_services
from pay_with_nano.database import db
from pay_with_nano.core.models import User, Transaction


def validated(username, password):
    user = User.query.filter_by(username=username).first()

    if user and rpc_services.unlock_wallet(user.wallet_id, password):
        rpc_services.lock_wallet(user.wallet_id)
        return True

    return False


def initialise_user(username, password, email):
    # make new wallets
    wallet_id = rpc_services.create_new_wallet()
    transition_wallet_id = rpc_services.create_new_wallet()

    # generate an address for refund
    refund_address = rpc_services.create_new_account(wallet_id)

    # change password
    rpc_services.change_wallet_password(wallet_id, password)

    # lock wallet
    rpc_services.lock_wallet(wallet_id)

    # save user to database
    new_user = User(
        username=username,
        wallet_id=wallet_id,
        transition_wallet_id=transition_wallet_id,
        email=email,
        refund_address=refund_address
    )
    db.session.add(new_user)
    db.session.commit()


def change_receiving_address(user, new_address):
    user.receiving_address = new_address
    db.session.commit()


def change_pin(user, new_pin):
    user.pin = new_pin
    db.session.commit()


def get_user_transactions(user):
    return Transaction.query.filter(Transaction.user_id == user.id).all()[::-1]


def get_transaction_from_id(transaction_id):
    return Transaction.query.filter(Transaction.id == transaction_id).first()


def can_refund(user, transaction):
    return transaction is not None and \
           transaction.status == 'success' and \
           transaction.user_id == user.id and \
           Decimal(transaction.amount_nano) <= rpc_services.get_balance_nano(user.refund_address)


def refund(user, password, transaction):
    rpc_services.unlock_wallet(user.wallet_id, password)
    block_hash = rpc_services.send_nano(
        wallet_id=user.wallet_id,
        source=user.refund_address,
        destination=transaction.source,
        amount_nano=transaction.amount_nano
    )
    rpc_services.lock_wallet(user.wallet_id)
    if block_hash:
        transaction.status = 'refunded'
        db.session.commit()
    return block_hash


def generate_seed(user):
    return hashlib.sha224(user.wallet_id.encode('utf-8')).hexdigest()
