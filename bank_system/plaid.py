import flask as f
import os
from plaid import Client
import requests

app = f.Blueprint('bank', __name__)

PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')
host = 'https://sandbox.plaid.com'

client = Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET, public_key=PLAID_PUBLIC_KEY, environment='sandbox')

@app.route('/login', methods=['GET', 'POST'])
def login():
    page = 'bank_system/login_form.html'
    if f.request.method == 'GET':
        return f.render_template(page)

    if f.request.method =='POST':
        search_text = f.request.form['bank_name']
        institutions = get_bank_suggestions(search_text)
        return f.render_template(page, options = institutions )


class Insitution:
    name = None
    iden = None
    def __init__(self, name, iden):
        self.name = name
        self.iden = iden





def get_bank_suggestions(text):
    headers = {'Content-type': 'application/json'}

    def search(text):
        data = {'query': text,
                'products': ['transactions', 'auth'],
                'public_key': PLAID_PUBLIC_KEY,
                }
        x = requests.post(host + '/institutions/search', json=data, headers=headers)
        return x.json()

    x = search(text)

    results = x['institutions']

    insitutions = []
    for result in results:
        name = result['name']
        iden = result['institution_id']
        inst = Insitution(name, iden)
        insitutions.append(inst)

    return insitutions
