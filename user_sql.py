from sql import do_sql, read_sql
import time




def make_database():
    ip_table = '''
    create table IF NOT EXISTS ip_address (
    ip TEXT primary key not null,
    login_attempts INTEGER not null,
    last_attempt_time INTEGER not null
    )
    '''
    do_sql(ip_table)
    
    account_table = '''
    create table IF NOT EXISTS account (
    username TEXT primary key not null,
    password INTEGER not null,
    role INTEGER not null
    )
    
    '''
    do_sql(account_table)    
    admin_account = '''
    replace into account (username, password, role) values('admin', '383b39a5c9a275ae22c0ec1ba427716b5826fbf15ad1e168b2886fc6', 'admin')
    '''
    do_sql(admin_account)
    
make_database()
    



def record_login_attempt(ip_address):
    now = time.time()
    get_attempts_sql = 'select * from ip_address where ip = \'{}\''''.format(ip_address)
    data = read_sql(get_attempts_sql)
    
    if len(data) == 0:
        new_record_sql = "insert into ip_address (ip, login_attempts, last_attempt_time) values ( '{}' , '0', '{}')".format(ip_address, now)
        do_sql(new_record_sql)
    
    if len(data) == 1:
        data.set_index('ip', inplace = True)
        
        last_time = int(data.loc[ip_address, 'last_attempt_time'])
        current = data.loc[ip_address, 'login_attempts'] + 1
        increment_sql = ' UPDATE ip_address SET login_attempts = {}, last_attempt_time = {} WHERE ip = \'{}\''.format(current,now, ip_address)
        do_sql(increment_sql)
        return current, now -  last_time
    
    return 0, 9999


def clear_login_attempts(ip_address):
    sql = 'update ip_address set login_attempts = 0 where ip = \'{}\''.format(ip_address)
    do_sql(sql)
    return True


def password_check(username, password):
    sql = 'select username, password from account where username = \'{}\' '.format(username) 
    data = read_sql(sql)
    if len(data) == 0:
        raise ValueError('No Such User')
    data.set_index('username', inplace = True)
    
    if data.loc[username, 'password'] != password:
        raise ValueError('Wrong Password')
        
def make_user(username, password, role):
    if len(username) > 50:
        raise ValueError('Max Length of username is 50 chars, your password however, can be as long as you want it to be.')
    sql = "insert into account (username, password, role) values ('{}', '{}', '{}')".format(username, password, role)
    do_sql(sql)
    return 


def get_role(username):
    sql = 'select username, role from account where username = \'{}\' '.format(username)
    data = read_sql(sql)
    assert(len(data) == 1)
    data.set_index('username', inplace = True)
    return data.loc[username, 'role']