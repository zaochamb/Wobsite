import random
import flask as f
import settings
from flask_sslify import SSLify
from flask import Flask, request, render_template, abort

# blueprint imports
from phone_system import phone
from login_system import login
from article_system import article
from product_system import product
from resource_system import resources
from bank_statement_system import plaid

# Register blueprints
def get_app():
    app = Flask(__name__)
    app.register_blueprint(login.app)
    app.register_blueprint(phone.app)
    app.register_blueprint(article.app)
    app.register_blueprint(product.app)
    app.register_blueprint(resources.app, url_prefix='/resources')
    app.register_blueprint(plaid.app, url_prefix='/bank')
    app.secret_key = str(random.random() + random.random())
    app.url_map.strict_slashes = False
    return app


app = get_app()
sslify = SSLify(app)

if __name__ == "__main__":
    app = get_app()


@app.route('/get_image')
def get_image():
    kind = request.args.get('kind', '')
    image_path = request.args.get('image_path', None)
    image_path = image_path.replace('%20', ' ').replace('+', ' ')
    image_path = image_path.replace('.html', '')
    image_path = kind + image_path
    for ext in ['.png', '.jpg']:
        try:
            return f.send_from_directory('static', filename=image_path + ext)
        except Exception as E:
            pass

    return f.send_from_directory('static', filename=kind + '/default.png')




@app.route('/')
def home():
    return render_template('home.html')

@app.route('/apply')
def apply():
    return contact(greeting = "Apply Now!")

@app.route('/contact')
def contact(greeting = False):
    if greeting != False:
        return render_template('apply.html', greeting = greeting)
    return render_template('apply.html')


@app.route('/employee')
def employee():
    return render_template('employee.html')

@app.route('/partners')
def partners():
    return render_template('partners.html')

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/search')
def search(query = ''):
    return render_template('search_results.html', query = query)

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return f.send_from_directory(app.static_folder, request.path[1:])


def get_links():
    import xml.etree.ElementTree as ET
    import pathlib
    file = settings.get_dir_static(pathlib.Path('sitemap.xml'))
    links = []

    root = ET.parse(file).getroot()
    for child in root:
        for subchild in child:
            if 'https' in subchild.text:
                links.append(subchild.text)

    return links


@app.route('/address')
def get_address():
    return render_template('address.html')

@app.errorhandler(404)
def page_not_found(e):
    links = get_links()
    import difflib
    result = difflib.get_close_matches(request.url, links, n = 1, cutoff= 0)
    if len(result) == 1:
        result = result[0]
        return f.redirect(result, 301)
    if len(result) == 0:
        return 'Page Not Found', 404

if __name__ == "__main__":
        app.run(debug = True)
