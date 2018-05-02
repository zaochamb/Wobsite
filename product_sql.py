
from sql import do_sql, read_sql

def make_database():
    product_sql = '''
    create table IF NOT EXISTS products (
    name TEXT primary key not null,
    description TEXT null,
    requirements TEXT null,
    steps TEXT null
    )
    '''
    do_sql(product_sql)
    
make_database()
    
def get_product_list():
    get_sql = 'select name from products'
    data = read_sql(get_sql)['name'].values
    return data


def save_product_details(name, values = {}):
    assert len(values) > 0
        
    if name in get_product_list():
        for key, value in values.items():
            if value != False:
                print(value)
                sql = ''' UPDATE products set {} = '{}' where name = '{}'  '''.format(key, value, name)
                do_sql(sql)
                
        return 'Updated'
    
    if name not in get_product_list():
        keys = ','.join(values.keys())
        vals = "','".join(values.values())
        sql = ''' insert into products (name,{}) values ('{}', '{}')'''.format(keys,name, vals)
        do_sql(sql)
        return 'inserted'
    
    
    
def get_product(name):
    get_sql ="select * from products where name = '{}'".format(name)
    data = read_sql(get_sql)
    return data

