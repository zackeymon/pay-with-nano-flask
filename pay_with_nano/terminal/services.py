from pay_with_nano.core import rpc_services
from pay_with_nano.database import db
from pay_with_nano.core.models import User


def validated(username, password):
    user = User.query.filter_by(username=username).first()

    if user and rpc_services.unlock_wallet(user.wallet_id, password):
        return True

    return False


def initialise_user(username, password, email):
    # make new wallet
    wallet_id = rpc_services.create_new_wallet()

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
        email=email,
        refund_address=refund_address
    )
    db.session.add(new_user)
    db.session.commit()
