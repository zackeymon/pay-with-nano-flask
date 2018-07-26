from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import InputRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', description='username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', description='********', validators=[InputRequired(), Length(min=4, max=32)])


class RegisterForm(FlaskForm):
    username = StringField('Username', description='username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', description='joe@blogg.com', validators=[InputRequired(), Length(min=4, max=32)])
    password = PasswordField('Password', description='********', validators=[InputRequired(), Length(min=4, max=32), EqualTo('re_password')])
    re_password = PasswordField('Repeat Password', description='********', validators=[InputRequired(), Length(min=4, max=32), EqualTo('password')])


class ChangeAddressForm(FlaskForm):
    new_address = StringField("New Address", description='xrb_', validators=[InputRequired()])


class RequestAmountForm(FlaskForm):
    amount = DecimalField('Amount', description='0.0')
    submit = SubmitField('Request')
