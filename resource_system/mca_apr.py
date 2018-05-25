import flask as f


def convert_calc():
    page_url = 'resource_system/convert_mca_to_apr.html'
    if f.request.method == 'GET':
        return f.render_template(page_url)
    if f.request.method == 'POST':
        time = f.request.form['time']
        fee = f.request.form['fee']

        time = int(time)
        fee = float(fee)

        apr = calculate_mca_to_apr(time, fee)

        apr = '{:,.2f} %'.format(apr)
        return f.render_template(page_url, apr = apr)


def calculate_mca_to_apr(time, fee):
    fee = fee -1
    times_per_year = 240/time
    apr = times_per_year * fee
    return apr * 100


def compare_calc():
    page_url = 'resource_system/mca_calculator.html'
    if f.request.method == 'GET':
        return f.render_template(page_url)

    if f.request.method == 'POST':
        form  = {}
        for thing in ['money', 'time', 'fee']:
            for pre  in ['x_', 'y_']:
                name = pre + thing
                form[name] = float(f.request.form[name])


        x_money = form['x_money']
        x_time = form['x_time']
        x_fee = form['x_fee']

        y_money = form['y_money']
        y_time = form['y_time']
        y_fee = form['y_fee']

        x = MCA(x_money, x_time, x_fee)
        y = MCA(y_money, y_time, y_fee)

        return f.render_template(page_url, mcas = [x, y])


class MCA():
    daily = None
    cost = None

    def __init__(self, money, time, fee):
        self.daily = money/time
        self.cost = fee * money
        self.daily = '$ {:,.2f}'.format(self.daily)
        self.cost = '$ {:,.2f}'.format(self.cost)