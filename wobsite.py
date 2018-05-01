import random
import flask as f
from flask_sslify import SSLify
from flask import Flask, request, render_template
import phone





app = Flask(__name__)
#sslify = SSLify(app)
app.secret_key = str(random.random() + random.random())



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/employee')
def employee():
    return render_template('employee.html')


@app.route('/get-estimate-or-apply')
def get_estimate_or_apply():
    return render_template('get_estimate_or_apply.html')


@app.route('/partners')
def partners():
    return render_template('partners.html')



#------------------------------PHONE SYSTEM----------------------#

@app.route('/ivr')
def ivr():
    return phone.ivr(request)

@app.route('/call_router/', methods = ['GET', 'POST'])
def call_router():
    return phone.call_router(request)
    
if __name__ == "__main__":
    app.run()