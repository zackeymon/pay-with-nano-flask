from flask import Flask
from database import db, DATABASE_URI
from api.controllers import api
from api.models import User
from payment.controllers import pay
from terminal.controllers import terminal

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yolo'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False

db.app = app
db.init_app(app)
db.create_all()

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(pay, url_prefix='/pay')
app.register_blueprint(terminal)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
