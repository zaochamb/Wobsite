import sqlite3
import pandas as pd
import settings



database_name = settings.get_database_dir('database.db')

    
def do_sql(sql):
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()

def read_sql(sql):
    with sqlite3.connect(database_name) as con:
        data = pd.read_sql(sql, con)
    return data

