import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask
from pay_with_nano.database import db
from pay_with_nano.config import SQLALCHEMY_DATABASE_URI
from pay_with_nano.api.controllers import api
from pay_with_nano.payment.controllers import pay
from pay_with_nano.terminal.controllers import terminal

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
