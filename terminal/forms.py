from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    username = StringField('Username', description='username')
    password = PasswordField('Password', description='********')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    username = StringField('Username', description='username')
    email = StringField('Email', description='joe@blogg.com')
    password = PasswordField('Password', description='********')
    re_password = PasswordField('Repeat Password', description='********')
    submit = SubmitField('Sign up')
