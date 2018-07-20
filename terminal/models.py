from database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(32), unique=True)
    receiving_address = db.Column(db.String(32), unique=True)

    wallet_id = db.Column(db.String(80), unique=True)
    refund_public_key = db.Column(db.String(80), unique=True)
