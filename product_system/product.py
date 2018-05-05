import flask as f
from flask import Flask, request, render_template, abort
from login_system import login_tools
from product_system import product_tools
import settings
import pandas as pd
import pathlib
app = f.Blueprint('product', __name__)



@app.route('/get-estimate-or-apply')
@app.route('/products')
@app.route('/products/<product>')
def products(product=''):
    if product == '':
        prods = get_product_list()
        return render_template('products.html', products = prods.index)
    return render_template('products/{}.html'.format(product))


def get_product_list():
    dir = settings.get_dir(pathlib.Path('product_system','products.csv'))
    data = pd.read_csv(dir)
    data = data.set_index('Product')
    return data