
from product_system import product_sql

def get_product_list():
    return product_sql.get_product_list()


def save_product_details(name, values = {}):
    return product_sql.save_product_details(name, values)


def get_product(name):
    return product_sql.get_product(name)