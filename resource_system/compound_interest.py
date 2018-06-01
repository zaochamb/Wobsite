import flask as f
import numpy as np


def main_calc():
    page_url = 'resource_system/compound_interest_calculator.html'
    if f.request.method == 'GET':
        return f.render_template(page_url)
    if f.request.method == 'POST':
        p = f.request.form['p']
        r = f.request.form['r']
        n = f.request.form['n']
        t = f.request.form['t']

        p = float(p)
        r = float(r)/100
        n = float(n)
        t = float(t)
        try:
            inflation = float(f.request.form.get('inflation', 0))
        except ValueError:
            inflation = 0

        if inflation != 0:
            saved,x = calculate(p, inflation/365, 365, t )
            cost ,pmt_size= calculate(p, r, n, t)
            return f.render_template(page_url, cost = cash_format(cost),
                                     pmt_size = cash_format(pmt_size),
                                     interest_rate = '{:.2f} %'.format(r * 100), inflation_savings = cash_format(saved), real_cost = cash_format(cost - saved ))

        cost, pmt_size = calculate(p, r, n, t)
        return f.render_template(page_url, cost=cash_format(cost),
                                 pmt_size=cash_format(pmt_size),
                                 interest_rate='{:.2f} %'.format(r * 100))



def cash_format(num):
    return '$ {:,.0f}'.format(num)


def get_payment(i, a, n):
    p = i * a / (1 - (1 + i) ** -n)
    return p


def get_cost(periods, interest, initial, payment):
    owed = initial
    cost = 0
    last_owed = owed

    while owed > 0:

        owed = owed * (1 + interest)
        cost = cost + last_owed - owed

        if payment > owed:
            payment = owed
        owed = owed - payment
        if owed > last_owed:
            return np.inf
        last_owed = owed

    return cost


def calculate(p, r, n, t):
    periods = n * t
    interest = r / n
    initial = p
    pmt_size = get_payment(interest, initial, periods)

    cost = get_cost(periods, interest, initial, pmt_size)

    return -1  * cost, pmt_size


