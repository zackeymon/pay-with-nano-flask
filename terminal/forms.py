from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField


class PaymentForm(FlaskForm):
    address = StringField('address')
    amount = DecimalField('amount')
