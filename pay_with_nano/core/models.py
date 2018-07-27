from flask_login import UserMixin

from pay_with_nano.database import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    timestamp = db.Column(db.String(20))
    success = db.Column(db.Boolean)
    from_address = db.Column(db.String(80))
    to_address = db.Column(db.String(80))
    amount = db.Column(db.String(20))
    hash = db.Column(db.String(80))

    # TODO: primary currency

    def __init__(self, **kwargs):
        super(Transaction, self).__init__(**kwargs)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(32), unique=True)

    receiving_address = db.Column(db.String(32))
    pin = db.Column(db.String(4))

    wallet_id = db.Column(db.String(80), unique=True)
    refund_address = db.Column(db.String(80), unique=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.username
