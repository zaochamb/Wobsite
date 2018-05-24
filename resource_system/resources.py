import flask as f

from resource_system import calculator

app = f.Blueprint('resources', __name__)


@app.route('/')
def resources():
    return f.render_template('/resource_system/resources.html')


@app.route('/compound_interest_calculator', methods=['GET', 'POST'])
def compound_interest_calculator():
    return calculator.compound_interest_calculator()
