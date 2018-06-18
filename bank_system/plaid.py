import flask as f
import os
from plaid import Client


app = f.Blueprint('bank', __name__)

PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')

client = Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET, public_key=PLAID_PUBLIC_KEY, environment='sandbox')

@app.route('/login', methods=['GET', 'POST'])
def login():
    page = 'bank_system/login_form.html'
    if f.request.method == 'GET':
        return f.render_template(page)

    if f.request.method =='POST':
        search_text = f.request.form['bank_name']
        bank_suggestions = get_bank_suggestions(search_text)
        return f.render_template(page, options = bank_suggestions )


def get_bank_suggestions(text):
    return ['option1', 'option2', text]