from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, SelectField, PasswordField
from wtforms.validators import InputRequired, NumberRange, Length

from pay_with_nano.core.models import Transaction


class PaymentForm(FlaskForm):
    address = StringField('Address', description='xrb_')
    amount = DecimalField('Amount', description='0.0', validators=[InputRequired(), NumberRange(min=0.0)])
    submit = SubmitField('Pay me')


class MerchantRequestForm(FlaskForm):
    currency = SelectField('Base Currency', choices=Transaction.SUPPORTED_CURRENCIES)
    amount = DecimalField('Amount', description='0.0', validators=[InputRequired(), NumberRange(min=0.0)])
    pin = PasswordField('PIN', description='****', validators=[InputRequired(), Length(min=4, max=4)])
