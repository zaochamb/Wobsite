import flask as f
from flask import Flask, request, render_template, abort
from login_system import login_tools
from product_system import product_tools

app = f.Blueprint('product', __name__)



@app.route('/get-estimate-or-apply')
@app.route('/products')
@app.route('/products/<product>')
def products(product=''):
    if product == '':
        products = ['a', 'b', 'c', 'd']
        return render_template('products.html', products = products)
    return render_template('products/{}.html'.format(product))