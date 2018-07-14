from flask import Blueprint, request, render_template
from api.services import validated


terminal = Blueprint('terminal', __name__, static_folder='static', template_folder='templates')


@terminal.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')

    # POST
    if validated(username=request.form['username'], password=request.form['password']):
        return 'Logged in!'
    else:
        return 'Wrong username or password!'
