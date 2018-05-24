import flask as f

def compound_interest_calculator():
    page_url = 'resource_system/compound_interest_calculator.html'
    if f.request.method == 'GET':
        return f.render_template(page_url)
    if f.request.method == 'POST':
        p = f.request.form['p']
        r = f.request.form['r']
        n = f.request.form['n']
        t = f.request.form['t']

        cost ,pmt_size= calculate(p, r, n, t)
        return f.render_template(page_url, cost = cash_format(cost), pmt_size = cash_format(pmt_size))


def cash_format(num):
    return '$ {:,.0f}'.format(num)


def calculate(p, r, n, t):
    p = float(p)
    r = float(r)
    n = float(n)
    t = float(t)
    a = p * (1 + r/n)**(n * t)

    cost = a - p
    pmt_size = a/t

    return cost, pmt_size
