import flask as f
from flask import render_template

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
        return render_template('product_system/products.html', products=prods)
    if product == 'revenue_funding':
        return f.redirect(
            'https://forms.zohopublic.com/virtualoffice9660/form/CommonApp/formperma/CA7AF9_f11jAbB47fmCb4Jham')

    prod_text = product.replace('_', ' ').title()
    return f.redirect('/contact', msg = 'STEP 1: Begin Your Application for {} by filling out this form:'.format(prod_text))


def get_product_list():
    dir = settings.get_dir_static(pathlib.Path('product_system', 'products.csv'))
    data = pd.read_csv(dir)
    data = data.set_index('product')
    data = data.sort_index()
    prods = []

    for index in data.index:
        prods.append(make_product(index, data.loc[index]))
    return prods


def make_product(name, series):
    requirements = series['requirements']
    description = series['description']
    prod = Product(name, requirements, description)
    return prod


class Product():
    name = None
    requirements = None
    description = None
    url = None

    def __init__(self, name, requirements, description):
        self.name = name
        self.requirements = requirements
        self.description = description
        self.url = 'products/' + name.lower().replace(' ', '_') + ''
