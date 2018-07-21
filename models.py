from database import db


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
