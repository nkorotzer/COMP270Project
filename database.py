import sqlite3
import sys

db_name = "info.db"

def connect_to_database(db_str):
    con = None
    try:
        con = sqlite3.connect(db_str)
        cur = con.cursor()
    except:
        print('Error connecting to database')
     
    return con, cur

def create_user_table(cur):
    # check if table exists
    print('Check if user table exists in the database:')
    sql = """SELECT name FROM sqlite_master WHERE type='table' AND name='user';"""
    listOfTables = cur.execute(sql).fetchall()
     
    if listOfTables == []:
        print('Table not found, creating...')
        sql = "CREATE TABLE user(username, password, pkey, msgs)"
        cur.execute(sql)
    else:
        print('Table found!')

def delete_user_table(cur):
    print('Deleting user table')
    sql = "DROP TABLE user"
    try:
        cur.execute(sql)
    except:
        print('Error while deleting table')
    
    return



def main():
    con, cur = connect_to_database(db_name)
    if con == None:
        sys.exit("Connection to database failed to establish")
    
    create_user_table(cur)
    

    res = cur.execute("SELECT name FROM sqlite_master")
    print(res.fetchone())
    
    #delete_user_table(cur)
    
    print("check")

if __name__ == "__main__":
    main()