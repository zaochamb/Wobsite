import flask as f
from login_system import login_tools
app = f.Blueprint('login', __name__)

from functools import wraps


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if f.request.method == 'GET':
        name = login_tools.get_username(f.session)
        if name == False:
            return f.render_template('login_system/login.html')
        if name != False:
            return logout()

    if f.request.method == 'POST':
        return login_tools.login_url(f.request, f.session)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if f.request.method == 'POST':
        try:
            del f.session['username']
        except KeyError:
            pass
        return 'logged out'
    if f.request.method == 'GET':
        return f.render_template('login_system/logout.html')


def requires_login(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
            name = login_tools.get_username(f.session)
            if name:
                return func(*args, **kwargs)
            return f.redirect('/login')
    return decorated_view


