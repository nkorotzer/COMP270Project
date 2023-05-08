import sqlite3
import sys

db_name = "info.db"

def connect_to_database(db_str):
    con = None
    try:
        con = sqlite3.connect(db_str)
        cur = con.cursor()
    except sqlite3.Error as error:
        print('Error connecting to database:',error)
     
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

def delete_user_table_contents():
    con, cur = connect_to_database(db_name)
    print('Deleting user table contents')
    sql = "DELETE FROM user;"
    try:
        cur.execute(sql)
        con.commit()
    except sqlite3.Error as error:
        print('Error while deleting table contents: ',error)
    
    cur.close()
    con.close()
    return

def add_user(username, password, pkey):
    con, cur = connect_to_database(db_name)
    sql =   """INSERT INTO user
            (username,password,pkey,msgs)
            VALUES
            (?, ?, ?, ?);"""
    data_tuple = (username, password, pkey, '')
    try:
        cur.execute(sql, data_tuple)
        con.commit()
        ret = 'success'
    except sqlite3.Error as error:
        print('Error adding user: ',error)
        ret = 'fail'

    cur.close()
    con.close()
    return ret

def print_all_users():
    con, cur = connect_to_database(db_name)
    cur.execute("SELECT * FROM user")
    print(cur.fetchall())
    cur.close()
    con.close()

def does_user_exist(username):
    con, cur = connect_to_database(db_name)
    sql = """SELECT username FROM user WHERE username=?"""
    try:
        cur.execute(sql,(username,))
        result = cur.fetchone()
    except sqlite3.Error as error:
        print('Error checking for user:',error)
        cur.close()
        con.close()
        return False
    if result:
        cur.close()
        con.close()
        print(f'User \'{username}\' already exists')
        return True
    else:
        cur.close()
        con.close()
        print(f'User \'{username}\' does not exist')
        return False

def main():
    con, cur = connect_to_database(db_name)
    if con == None:
        sys.exit("Connection to database failed to establish")
    
    create_user_table(cur)
    

    res = cur.execute("SELECT name FROM sqlite_master")
    print(res.fetchone())

    while True:
        print_all_users()
        uname = input('Enter username: ')
        if uname == 'exit':
            break
        elif uname == 'delete':
            delete_user_table_contents()
        else:
            if does_user_exist(uname):
                print('user already exists')
            else:
                add_user(uname, 'none for now', 'will add later')
    
    print("check")

if __name__ == "__main__":
    main()