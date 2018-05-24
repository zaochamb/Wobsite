import flask as f


def main_calc():
    page_url = 'resource_system/convert_mca_to_apr.html'
    if f.request.method == 'GET':
        return f.render_template(page_url)
    if f.request.method == 'POST':
        time = f.request.form['time']
        fee = f.request.form['fee']

        time = int(time)
        fee = float(fee)

        apr = calculate(time, fee)

        apr = '{:,.2f} %'.format(apr)
        return f.render_template(page_url, apr = apr)


def calculate(time, fee):
    fee = fee -1
    times_per_year = 240/time
    apr = times_per_year * fee
    return apr * 100