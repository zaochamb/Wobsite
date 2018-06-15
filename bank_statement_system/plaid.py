import flask as f
import os
from plaid import Client


app = f.Blueprint('bank', __name__)

PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')

@app.route('/')
def home():
    return PLAID_CLIENT_ID

@app.route('/test')
def test():
    return 'HELLO WORLD'