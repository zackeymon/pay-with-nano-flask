from flask import Blueprint, request, render_template

terminal = Blueprint('terminal', __name__, static_folder='static', template_folder='templates')


@terminal.route('/login', methods=['GET', 'POST'])
def login_page():
    return render_template('login.html')
