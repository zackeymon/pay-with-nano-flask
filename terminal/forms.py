from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', description='username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', description='********', validators=[InputRequired(), Length(min=4, max=32)])
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    username = StringField('Username', description='username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', description='joe@blogg.com', validators=[InputRequired(), Length(min=4, max=32)])
    password = PasswordField('Password', description='********', validators=[InputRequired(), Length(min=4, max=32), EqualTo('re_password')])
    re_password = PasswordField('Repeat Password', description='********', validators=[InputRequired(), Length(min=4, max=32), EqualTo('password')])
    submit = SubmitField('Sign up')


class ChangeAddressForm(FlaskForm):
    new_address = StringField("Address", description='xrb_', validators=[InputRequired()])
    submit = SubmitField('Change')
