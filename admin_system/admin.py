import flask as f
from flask import Flask, request, render_template, abort
from login_system import login_tools
import product_tools

app = f.Blueprint('admin', __name__)




@app.route('/admin', methods=['POST', 'GET'])
def admin_panel():
    if request.method == 'GET':
        name = login_tools.get_username(f.session)
        if name == False:
            return render_template('login_system/login.html')
        role = login_tools.get_role(name)
        if role != 'admin':
            return login_tools.alert('Admin Only.')
        if role == 'admin':
            cols = product_tools.get_product('').columns
            return render_template('admin_system/admin.html', product_columns = cols)
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
        