from flask import Flask
from api.controllers import api
from payment.controllers import pay
from terminal.controllers import terminal

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(pay, url_prefix='/pay')
app.register_blueprint(terminal)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(threaded=True)
