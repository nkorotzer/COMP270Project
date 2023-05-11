import sqlite3
import sys
import nacl.pwhash
import nacl.exceptions
import datetime

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
        sql = "CREATE TABLE user(username, password, pkey, msgs, date)"
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
            (username,password,pkey,msgs,date)
            VALUES
            (?, ?, ?, ?, ?);"""
    data_tuple = (username, password, pkey, '', datetime.datetime.now())
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

def validate_user(username, password):
    con, cur = connect_to_database(db_name)
    sql = """SELECT password 
            FROM user 
            WHERE username=? AND password != ''"""
    try:
        cur.execute(sql,(username,))
        result = cur.fetchone()
    except sqlite3.Error as error:
        print('Error finding password: ', error)
    
    password_hash = result[0]
    print('Password hash = ', password_hash)
    print('Password = ', password)
    try:
        result = nacl.pwhash.scrypt.verify(password_hash, password.encode())
    except nacl.exceptions.CryptoError as error:
        print('error verifying password: ', error)
    
    cur.close()
    con.close()
    return result

def get_user_pub_key(username: str) -> bytes:
    con, cur = connect_to_database(db_name)
    sql = """SELECT pkey 
            FROM user 
            WHERE username=? AND pkey != ''"""
    try:
        cur.execute(sql,(username,))
        result = cur.fetchone()
    except sqlite3.Error as error:
        print(f'Error finding {username}\'s public key: ', error)

    cur.close()
    con.close()    
    return result[0]

def add_message(recipient: str, encrypted_message: bytes):
    con, cur = connect_to_database(db_name)
    sql =   """INSERT INTO user
            (username,password,pkey,msgs,date)
            VALUES
            (?, ?, ?, ?, ?);"""
    data_tuple = (recipient, '', '', encrypted_message, datetime.datetime.now())
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

def read_all_messages(username):
    con, cur = connect_to_database(db_name)
    sql = """SELECT msgs 
            FROM user 
            WHERE username=? AND pkey == ''
            ORDER BY date"""
    try:
        cur.execute(sql,(username,))
        ret = cur.fetchall()
        print('ret: ',ret)
    except sqlite3.Error as error:
        print('Error reading user messages: ', error)
        ret = 'Error'
    if not ret:
        return b'None'
    else:
        return ret

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