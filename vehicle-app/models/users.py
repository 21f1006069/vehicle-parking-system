import sqlite3
import bcrypt
from config import DATABASE_PARKING

def create_user_table():
    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email Text NOT NULL UNIQUE,
            password Text NOT NULL,
            name Text NOT NULL,
            address Text NOT NULL,
            pincode Text NOT NULL,
            phone_no Text NOT NULL,
            role Text DEFAULT 'user'
        )
        '''
    )

    cur.execute("SELECT * FROM users WHERE email = ?", ("admin@parking.com",))
    if not cur.fetchone():
        hashed_password = bcrypt.hashpw("admin@123".encode('utf-8'), bcrypt.gensalt())
        cur.execute(
            '''
                INSERT INTO USERS (email, password, name, address, pincode, phone_no,role) VALUES (?,?,?,?,?,?,?) 
            ''',('admin@parking.com', hashed_password, 'Admin','Chennai', '123456', '1234567890','admin')
        )

        print("Admin Created with Email - admin@parking.com and PASSWORD - admin@123")

    connection.commit()
    connection.close()


def check_user(email):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()
    res = cur.execute(
        '''    
            SELECT email FROM USERS where email=?
        ''', (email,)
    )

    user = res.fetchone()
    connection.commit()
    connection.close()
    if user:
        return True
    else:
        return False

    
def register_user(email, hashedpassword, fullname, address, pincode,phone_no):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()
    res = cur.execute(
        '''
            INSERT INTO users (email, password, name, address, phone_no,pincode) VALUES (?,?,?,?,?,?)
        ''',(email, hashedpassword, fullname, address, phone_no,pincode)
    )

    connection.commit()
    connection.close()

def fetch_user(email,password):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()
    cur.execute(
        '''
            SELECT * FROM USERS WHERE email = ?
        ''',(email,)        
    )

    user = cur.fetchone()
    if user:
        hashed_password = user[2]
        pass_correct = bcrypt.checkpw(password.encode('utf-8'), hashed_password)  
        if pass_correct:
            return user

    return None

