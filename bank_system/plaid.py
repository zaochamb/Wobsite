import flask as f
from flask import render_template
from flask import request
from flask import jsonify
import os
import datetime
import plaid


app = f.Blueprint('bank', __name__)

PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')
PLAID_ENV  = 'sandbox'
client = plaid.Client(client_id = PLAID_CLIENT_ID, secret=PLAID_SECRET,
                  public_key=PLAID_PUBLIC_KEY, environment=PLAID_ENV)

@app.route("/begin")
def begin():
   return render_template('bank_system/begin.html', plaid_public_key=PLAID_PUBLIC_KEY, plaid_environment=PLAID_ENV)


access_token = None
public_token = None
item_id = None

@app.route("/get_access_token", methods=['POST'])
def get_access_token():
  global access_token
  global public_token
  global item_id

  public_token = request.form['public_token']
  exchange_response = client.Item.public_token.exchange(public_token)
  item_id = exchange_response['item_id']

  access_token = exchange_response['access_token']

  return jsonify(exchange_response)


@app.route("/test")
def test():
    global access_token
    global public_token
    global item_id
    result = ''' accesstoken:{}
     publictoken:{}
      item_id: {}'''.format(access_token, public_token, item_id)
    return  result