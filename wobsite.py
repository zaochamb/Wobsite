import random
import flask as f
from flask_sslify import SSLify
from flask import Flask, request, render_template, abort

# blueprint imports
from phone_system import phone
from login_system import login
from article_system import article
from admin_system import admin
from product_system import product

# Register blueprints
def get_app():
    app = Flask(__name__)
    app.register_blueprint(login.app)
    app.register_blueprint(phone.app)
    app.register_blueprint(article.app)
    app.register_blueprint(admin.app)
    app.register_blueprint(product.app)
    app.secret_key = str(random.random() + random.random())
    app.url_map.strict_slashes = False
    return app

 
app = get_app()
sslify = SSLify(app)


if __name__ == "__main__":
    app = get_app()

    


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<string:page_name>/')
def static_page(page_name):
    if page_name.lower() in ['employee', 'partners', 'privacy_policy']:
        return render_template('static/%s.html' % page_name)
    abort(404)


@app.route('/contact')
def contact():
    return f.redirect('https://forms.zohopublic.com/virtualoffice9660/form/EmailSubscription/formperma/EjHCagK__022JHhfA02F5_0g7')




    
if __name__ == "__main__":
        app.run(debug = True)
