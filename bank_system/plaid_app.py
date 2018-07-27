import flask as f
from flask import render_template
from flask import request
from flask import jsonify
import os
import requests
import plaid
import pandas as pd
from login_system.login import requires_login
from login_system import login_tools
from bank_system import bank_sql
app = f.Blueprint('bank', __name__)

PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')
PLAID_ENV  = 'development'
host = 'https://development.plaid.com'



client = plaid.Client(client_id = PLAID_CLIENT_ID, secret=PLAID_SECRET,
                  public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)


@app.route("/begin")
@requires_login
def begin():
    token, other = get_creds()

    message = 'Connected'
    if token is None:
        message = 'Not Connected'

    return render_template('bank_system/begin.html', plaid_public_key=PLAID_PUBLIC_KEY, plaid_environment=PLAID_ENV, message = message)


access_token = None
public_token = None
item_id = None


@app.route("/get_access_token", methods=['POST'])
@requires_login
def get_access_token():
  global public_token

  public_token = request.form['public_token']
  exchange_response = client.Item.public_token.exchange(public_token)
  item_id = exchange_response['item_id']

  access_token = exchange_response['access_token']

  username = login_tools.get_username(f.session)
  bank_sql.set_creds(username ,access_token, item_id)
  return render_template('bank_system/begin.html', message = 'Connected')

def get_creds():
    username = login_tools.get_username(f.session)
    access_token, item_id = bank_sql.get_creds(username)
    return access_token, item_id

@app.route('/get_banks', methods=['POST'])
@requires_login
def get_banks():
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
    end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')
    access_token, item_id = get_creds()

    data = {'client_id': PLAID_CLIENT_ID,
            'secret': PLAID_SECRET,
            'access_token': access_token,
            'start_date': start_date,
            'end_date': end_date,
            }

    x = requests.post(host + '/transactions/get', json=data).json()
    try:
        x = pd.DataFrame(x['transactions'])
    except KeyError:
        return 'NO TRANSACTIONS FOUND'

    resp = f.make_response(x.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


@app.route('/get_balance', methods=['POST'])
@requires_login
def get_balance():
    access_token, item_id = get_creds()
    data = {'client_id': PLAID_CLIENT_ID,
            'secret': PLAID_SECRET,
            'access_token': access_token,
            }

    x = requests.post(host + '/accounts/balance/get', json=data).json()
    result = ''
    for account in x['accounts']:
        name = account['name']
        balance = account['balances']['available']
        result = result + '\n  {} : {}'.format(name, balance)
    return render_template('bank_system/begin.html', message='Connected', balance = result)


@app.route('/get_routing', methods=['POST'])
@requires_login
def get_routing():
    access_token, item_id = get_creds()
    data = {'client_id': PLAID_CLIENT_ID,
            'secret': PLAID_SECRET,
            'access_token': access_token,
            }
    x = requests.post(host + '/auth/get', json=data).json()
    result = str(x['numbers'])
    '''
    result = str(x['numbers']['eft'])
  
    for ach in x['numbers']['ach']:
        account = ach['account']
        routing = ach['routing']
        wire = ach['wire_routing']
        result = result + '\naccount:{} \n routing:{} \n wire-routing{}\n'
        
    '''
    return render_template('bank_system/begin.html', message='Connected', routing = result)