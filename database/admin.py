import sqlite3
import pandas as pd
import hashlib
database_name = 'database.db'


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
    password text not null,
    role text not null
    )

    '''
    do_sql(account_table)

    bank_table = '''
    create table IF NOT EXISTS BANK (
    username TEXT primary key not null,
    access_token text not null,
    item_id text not null
    )
    '''
    do_sql(bank_table)


make_database()


def do_sql(sql):
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()

def hash(text):
    text = bytes(text, 'utf-8')
    return hashlib.sha224(text).hexdigest()

def read_sql(sql):
    with sqlite3.connect(database_name) as con:
        data = pd.read_sql(sql, con)
    return data


def create_user(username, password, role ):
    password = hash(password)
    sql = '''
    replace into account (username, password, role) values('{}', '{}', '{}')
    '''.format(username, password, role)
    return do_sql(sql)

def get_users(filter = ''):
    sql = 'SELECT * FROM ACCOUNT '
    if filter != '':
        sql = sql + ' WHERE ' + filter
    return read_sql(sql)

def remove_user(username):
    sql = "DELETE FROM ACCOUNT WHERE USERNAME = '{}'".format(username)
    do_sql(sql)
    sql2 = "  DELETE FROM BANK WHERE USERNAME =  '{}'".format(username)
    do_sql(sql2)

def options():
    '''Main interface'''
    text = '''
     Database Options
     1. Create New User
     2. Search Users
     3. Delete User
     
     4. Exit
     '''

    print(text)
    ans = int(input('Enter your Input'))
    if ans == 1:
        username = input('Username\n>>')
        password = input('Password\n>>')
        role = input('Role\n>>')
        create_user(username, password, role)

    if ans == 2:
        filters = input('Filters? Press ENTER FOR NONE\n>>')
        print(get_users(filters))

    if ans == 3:
        username = input('Which Username to delete?\n>>')
        remove_user(username)



    if ans == 4:
        return False
    return True



if __name__ == '__main__':
    switch = True
    while switch:
        switch = options()