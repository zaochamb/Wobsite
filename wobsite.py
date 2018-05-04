import random
import flask as f
from flask_sslify import SSLify
from flask import Flask, request, render_template, abort
import phone
import login_tools
import product_tools


app = Flask(__name__)
#sslify = SSLify(app)
app.secret_key = str(random.random() + random.random())
app.url_map.strict_slashes = False


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<string:page_name>/')
def static_page(page_name):
    if page_name.lower() in ['articles','contact', 'employee', 'partners', 'privacy_policy']:
        return render_template('static/%s.html' % page_name)
    abort(404)

@app.route('/get-estimate-or-apply')
@app.route('/products')
@app.route('/products/<product>')
def products(product=''):
    if product == '':
        products = ['a', 'b', 'c', 'd']
        return render_template('products.html', products = products)
    return render_template('products/{}.html'.format(product))



@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        name = login_tools.get_username(f.session)
        if name == False:
            return render_template('login/login.html')
        if name != False:
            return logout()
        
    if request.method == 'POST':
        return login_tools.login_url(request, f.session)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if request.method == 'POST':
        try:
            del f.session['username']
        except KeyError:
            pass
        return home()
    if request.method == 'GET':
        return render_template('login/logout.html')


@app.route('/contact')
def contact():
    return f.redirect('https://forms.zohopublic.com/virtualoffice9660/form/EmailSubscription/formperma/EjHCagK__022JHhfA02F5_0g7')



@app.route('/admin', methods=['POST', 'GET'])
def admin_panel():
    if request.method == 'GET':
        name = login_tools.get_username(f.session)
        if name == False:
            return render_template('login/login.html')
        role = login_tools.get_role(name)
        if role != 'admin':
            return login_tools.alert('Admin Only.')
        if role == 'admin':
            cols = product_tools.get_product('').columns
            return render_template('admin.html', product_columns = cols)
    if request.method == 'POST':
        name = login_tools.get_username(f.session)
        role = login_tools.get_role(name)
        if role == 'admin':
            cols = product_tools.get_product('').columns
            val_dict = {}
            for col in cols:
                val_dict[col] = request.form[col]
            name = val_dict['name']
            del val_dict['name']
            result = product_tools.save_product_details(name, val_dict)
            login_tools.alert('{}'.format(result))
            return f.redirect('/admin')
        
#------------------------------PHONE SYSTEM----------------------#

@app.route('/ivr')
def ivr():
    return phone.ivr(request)

@app.route('/call_router/', methods = ['GET', 'POST'])
def call_router():
    return phone.call_router(request)
    
if __name__ == "__main__":
    app.run()