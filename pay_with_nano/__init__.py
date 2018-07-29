import os

basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask, render_template
from pay_with_nano.database import db
from pay_with_nano.config import SQLALCHEMY_DATABASE_URI, MASTER_WALLET_ID
from pay_with_nano.api.controllers import api
from pay_with_nano.payment.controllers import pay
from pay_with_nano.terminal.controllers import terminal
from pay_with_nano.core import rpc_services

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yolo'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False

db.app = app
db.init_app(app)
db.create_all()

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(pay, url_prefix='/pay')
app.register_blueprint(terminal)

rpc_services.unlock_wallet(MASTER_WALLET_ID, '1111')


@app.errorhandler(401)
def unauthorised(e):
    return render_template('errors/page_401.html'), 401


@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/page_403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/page_404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/page_500.html'), 500
