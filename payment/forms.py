from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField


class PaymentForm(FlaskForm):
    address = StringField('Address', description='xrb_')
    amount = DecimalField('Amount', description='0.0')
