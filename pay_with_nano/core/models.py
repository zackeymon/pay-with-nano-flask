from flask_login import UserMixin
from pay_with_nano.database import db
from sqlalchemy_utils.types.choice import ChoiceType


class Transaction(db.Model):
    STATUSES = [
        ('success', 'Success'),
        ('cancelled', 'Cancelled'),
        ('timeout', 'Timeout'),
        ('refunded', 'Refunded')
    ]

    SUPPORTED_CURRENCIES = [
        ('nano', 'NANO'),
        ('usd', 'USD'),
        ('gbp', 'GBP'),
        ('eur', 'EUR'),
        ('jpy', 'JPY')
    ]

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    destination = db.Column(db.String(80))

    timestamp = db.Column(db.String(20))
    source = db.Column(db.String(80))
    amount_nano = db.Column(db.String(20))
    currency = db.Column(ChoiceType(SUPPORTED_CURRENCIES))
    amount = db.Column(db.String(20))
    status = db.Column(ChoiceType(STATUSES))
    hash = db.Column(db.String(80))

    def __init__(self, **kwargs):
        super(Transaction, self).__init__(**kwargs)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'timestamp': self.timestamp,
            'status': self.status,
            'source': self.source,
            'destination': self.destination,
            'amount_nano': self.amount_nano,
            'hash': self.hash
        }


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(32))

    receiving_address = db.Column(db.String(32))
    pin = db.Column(db.String(4))

    wallet_id = db.Column(db.String(80), unique=True)
    transition_wallet_id = db.Column(db.String(80), unique=True)
    refund_address = db.Column(db.String(80), unique=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.username
