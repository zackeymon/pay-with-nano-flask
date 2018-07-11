from flask import Flask
from api.api import api
from payment.pay import pay

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(pay, url_prefix='/pay')


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(threaded=True)
