import sqlite3
from config import DATABASE_PARKING
from datetime import datetime

def dict_rows(cursor):
    """Helper: Convert cursor.fetchall() output into list of dicts."""
    columns = [col[0] for col in cursor.description]  # column names
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_all_users():
    conn = sqlite3.connect(DATABASE_PARKING)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, email, name, address, pincode, phone_no, role
        FROM Users
    """)

    users = dict_rows(cursor) 
    conn.close()
    return users


def get_newly_created_lots():
    conn = sqlite3.connect(DATABASE_PARKING)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT lot_id, location_name, address, pincode, price, maxSpots
        FROM ParkingLot
        WHERE lot_id >= (SELECT MAX(lot_id) - 20 FROM ParkingLot)
    """)

    lots = dict_rows(cursor)
    conn.close()
    return lots


def get_user_last_visit(user_id):
    conn = sqlite3.connect(DATABASE_PARKING)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT parking_timestamp
        FROM Reserve_Parking_Spot
        WHERE user_id = ?
        ORDER BY parking_timestamp DESC
        LIMIT 1
    """, (user_id,))

    result = cursor.fetchone()
    conn.close()

    if not result:
        return None

    timestamp_str = result[0]

    try:
        return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")
    except:
        return None

def get_all_users_email():
    conn = sqlite3.connect(DATABASE_PARKING)
    cur = conn.cursor()

    cur.execute("SELECT user_id, email, name FROM Users")
    users = cur.fetchall()

    conn.close()
    return users


def get_user_monthly_data(user_id, year, month):
    conn = sqlite3.connect(DATABASE_PARKING)
    cur = conn.cursor()

    start = f"{year:04d}-{month:02d}-01 00:00"

    if month == 12:
        end = f"{year+1:04d}-01-01 00:00"
    else:
        end = f"{year:04d}-{month+1:02d}-01 00:00"

    cur.execute(
        """
        SELECT spot_id, lot_id, spot_id, vehicle_number,
               parking_timestamp, leaving_timestamp, parking_cost
        FROM Reserve_Parking_Spot
        WHERE user_id = ? AND parking_timestamp >= ? AND parking_timestamp < ?
        ORDER BY parking_timestamp
        """,
        (user_id,)
    )

    rows = cur.fetchall()
    print(rows)
    conn.close()

    return rows


def get_most_used_lot(user_id, year, month):
    conn = sqlite3.connect(DATABASE_PARKING)
    cur = conn.cursor()

    start = f"{year:04d}-{month:02d}-01 00:00"
    if month == 12:
        end = f"{year+1:04d}-01-01 00:00"
    else:
        end = f"{year:04d}-{month+1:02d}-01 00:00"

    
    cur.execute(
        """
        SELECT lot_id, COUNT(*) as c
        FROM Reserve_Parking_Spot
        WHERE user_id = ? AND parking_timestamp >= ? AND parking_timestamp < ?
        GROUP BY lot_id
        ORDER BY c DESC
        LIMIT 1
        """,
        (user_id,)
    )

    row = cur.fetchone()
    print(row)
    conn.close()

    return row if row else (None, 0)

def get_user_parking_history(user_id):
    conn = sqlite3.connect(DATABASE_PARKING)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT spot_id, lot_id, vehicle_number,
               parking_timestamp, leaving_timestamp, parking_cost
        FROM Reserve_Parking_Spot
        WHERE user_id = ?
        ORDER BY parking_timestamp DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows
