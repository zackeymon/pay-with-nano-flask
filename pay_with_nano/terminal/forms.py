from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import InputRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', description='username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', description='********', validators=[InputRequired(), Length(min=4, max=32)])


class RegisterForm(FlaskForm):
    username = StringField('Username', description='username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', description='joe@blogg.com', validators=[InputRequired(), Length(min=4, max=32)])
    password = PasswordField('Password', description='********',
                             validators=[InputRequired(), Length(min=4, max=32), EqualTo('re_password')])
    re_password = PasswordField('Repeat Password', description='********',
                                validators=[InputRequired(), Length(min=4, max=32), EqualTo('password')])


class ChangeAddressForm(FlaskForm):
    new_address = StringField("New Address", description='xrb_', validators=[InputRequired()])
    password = PasswordField('Password', description='********', validators=[InputRequired(), Length(min=4, max=32)])


class ChangePinForm(FlaskForm):
    pin = PasswordField('PIN', description='****',
                        validators=[InputRequired(), Length(min=4, max=4), EqualTo('re_pin')])
    re_pin = PasswordField('Repeat PIN', description='****',
                           validators=[InputRequired(), Length(min=4, max=4), EqualTo('pin')])
    password = PasswordField('Password', description='********', validators=[InputRequired(), Length(min=4, max=32)])
