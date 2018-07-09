from database import admin




def get_creds(username):
    creds = admin.read_sql("SELECT * FROM BANK WHERE USERNAME = '{}'".format(username))
    try:
        access_token =  creds.loc[0, 'access_token']
        item_id = creds.loc[0, 'item_id']
    except KeyError:
        access_token = None
        item_id = None
    return access_token, item_id

def set_creds(username,access_token, item_id ):
    new_record_sql = "insert into BANK (USERNAME, access_token, item_id) values ( '{}' , '{}', '{}')".format(username, access_token, item_id)
    admin.do_sql(new_record_sql)
