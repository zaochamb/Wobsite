import flask as f

from resource_system import compound_interest
from resource_system import mca_to_apr
app = f.Blueprint('resources', __name__)


@app.route('/')
def resources():
    return f.render_template('/resource_system/resources.html')

@app.route('/compound_interest_calculator', methods=['GET', 'POST'])
def compound_interest_calculator():
    return compound_interest.main_calc()

@app.route('/convert_revenue_funding_to_apr', methods = ['GET', 'POST'])
def convert_revenue_funding_to_apr():
    return mca_to_apr.main_calc()