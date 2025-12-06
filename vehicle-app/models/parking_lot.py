import sqlite3,datetime
from config import DATABASE_PARKING

def createParkingLot():
    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS ParkingLot (
            lot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_name TEXT NOT NULL,
            address TEXT NOT NULL,
            pincode TEXT NOT NULL,
            price INTEGER NOT NULL, 
            maxSpots INTEGER NOT NULL
        )
        '''
    )

    connection.commit()
    connection.close()

def insertParkingLot(locationName,address,pincode,pricePerHour,maxSpots):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
            INSERT INTO ParkingLot (location_name, address, pincode, price, maxSpots) VALUES (?,?,?,?,?)
        ''',(locationName, address, pincode, pricePerHour, maxSpots)
    )

    connection.commit()
    connection.close()

    return cur.lastrowid

def createParkingSpots():

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS ParkingSpots (
        lot_id INTEGER NOT NULL,
        spot_id INTEGER,  -- Optional: to identify spot within a lot
        status TEXT CHECK(status IN ('O', 'A')) NOT NULL DEFAULT 'A',
        FOREIGN KEY (lot_id) REFERENCES ParkingLot(lot_id) ON DELETE CASCADE
        );
    '''
    )

    connection.commit()
    connection.close()

def createReserveParkingSpot():

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
            '''
                CREATE TABLE IF NOT EXISTS Reserve_Parking_Spot (
                spot_id INTEGER NOT NULL,
                lot_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                vehicle_number TEXT NOT NULL,
                parking_timestamp DATETIME NOT NULL,
                leaving_timestamp DATETIME,
                parking_cost REAL,

                FOREIGN KEY (lot_id)  REFERENCES ParkingLot(lot_id)
                FOREIGN KEY (spot_id) REFERENCES ParkingSpots(spot_id),
                FOREIGN KEY (user_id) REFERENCES USERS(Id)
                );
            '''
    )

    connection.commit()
    connection.close()

def  createVehiclesTable():

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS Vehicles (
                user_id INTEGER NOT NULL,
                vehicle_number TEXT NOT NULL UNIQUE,
                vehicle_status TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            );
        '''
    )

    connection.commit()
    connection.close()

def insertParkingSpots(lot_id, i):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
            INSERT INTO ParkingSpots (lot_id, status, spot_id) VALUES (?,?,?) 
        ''',(lot_id, 'A', i)
    )

    connection.commit()
    connection.close()

def get_all_parking_lots():

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(''' Select * from ParkingLot ''')
    lots = cur.fetchall()

    connection.commit()
    connection.close()
    
    return lots

def get_all_parking_spots(lot_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute('''
                    Select * from ParkingSpots where lot_id = (?)
                ''', (lot_id,))
    
    spots = cur.fetchall()

    connection.commit()
    connection.close()

    return spots

def fetch_parking_lot(lot_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
            Select * from ParkingLot where lot_id = (?)
        ''',(lot_id,)
    )

    parkinglotData = cur.fetchone()

    connection.commit()
    connection.close()

    return parkinglotData

def updateParkinglot(locationName,address,pincode,pricePerHour,maxSpots,lot_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute ('''
                    Select maxSpots from ParkingLot where lot_id = (?)
                 ''',(lot_id,))
    
    old_maxSpots = cur.fetchone()[0]
   
    cur.execute('''
                UPDATE ParkingLot 
                SET location_name = ?, address = ?, pincode = ?, price = ?, maxSpots = ?
                WHERE lot_id = ?
            ''',(locationName,address,pincode,pricePerHour,maxSpots,lot_id)
            )
    
    print(lot_id)
    updated_rows = cur.rowcount
    print("Rows updated:", updated_rows)
    
    if old_maxSpots < int(maxSpots):

        newSpotsAdded = int(maxSpots) - old_maxSpots

        for i in range(old_maxSpots+1, int(maxSpots)+1):
            cur.execute('''
                            INSERT INTO PARKINGSPOTS VALUES(?,?,?)
                        ''',(lot_id, i,'A'))
        
    elif old_maxSpots > int(maxSpots):

        spots_to_remove = old_maxSpots - int(maxSpots)  

        # Count currently occupied spots
        cur.execute("SELECT COUNT(*) FROM ParkingSpots WHERE lot_id = ? AND status = 'O'", (lot_id,))
        occupied_spots = cur.fetchone()[0]

        # The new max cannot go below the number of occupied spots
        final_max = max(int(maxSpots), occupied_spots)
         
        cur.execute('''
            WITH to_delete AS (
                SELECT spot_id FROM ParkingSpots
                WHERE lot_id = ? AND status = 'A'
                ORDER BY spot_id
                LIMIT ?
            )
            DELETE FROM ParkingSpots
            WHERE lot_id = ? AND spot_id IN (SELECT spot_id FROM to_delete);
            ''', (lot_id, spots_to_remove, lot_id))
        
        cur.execute("UPDATE ParkingLot SET maxSpots = ? WHERE lot_id = ?", (final_max, lot_id))

    
    connection.commit()
    connection.close()
    return updated_rows  # Returns the number of rows updated, should be 1 if successful

def deleteParkingLotAndSpot(lot_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute( '''
                Delete from ParkingLot where lot_id = ?
                ''',(lot_id,))

    cur.execute('''
                    DELETE FROM ParkingSpots where lot_id = ?
                ''',(lot_id,))

    connection.commit()
    connection.close()

def deleteParticularParkingSpot(spot_id, lot_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute('''
                    DELETE FROM ParkingSpots 
                    where lot_id = ? AND spot_id = ?
                ''',(lot_id, spot_id))
    
    cur.execute('''
                    UPDATE ParkingLot
                    SET maxSpots = maxSpots - 1
                    WHERE lot_id = ? AND maxSpots > 0; 
                ''',(lot_id,))
    
    connection.commit()
    connection.close()

def getUsersData():

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute('''
                    SELECT * FROM USERS
                ''')
    
    users_data = cur.fetchall()
    
    connection.commit()
    connection.close()

    return users_data

def insertVehicleDetails(user_id, vehicle_number, vehicle_status):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
            INSERT INTO Vehicles (user_id, vehicle_number, vehicle_status) VALUES (?,?,?)
        ''',(user_id,vehicle_number,vehicle_status,)
    )

    connection.commit()
    connection.close()

def checkVehicleExists(vehicle_number):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
            select * from Vehicles where vehicle_number = ?
        ''', (vehicle_number,)
    )

    result = cur.fetchone()

    connection.commit()
    connection.close()

    if result:
        return True
    else:
        return False

#Method for table below the search box in User configuration
def get_availability_data():

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute( 
            '''
                select 
                pl.lot_id, 
                pl.address,
                Count(Case WHEN ps.status = 'A' THEN 1 END) As availabilty 
                from ParkingLot PL 
                Left Join 
                ParkingSpots PS ON PL.lot_id = PS.lot_id
                Group By
                PL.lot_id,PL.address
            '''
            )   
    
    result = cur.fetchall()
    connection.commit()
    connection.close()

    return result

def fetchOneParkingSpot(lot_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
                '''
                    select spot_id from ParkingSpots 
                    where lot_id = (?) and status = 'A'
                ''',(lot_id,)
    )

    spot_id = cur.fetchone()
    connection.commit()
    connection.close()

    return spot_id

def fetchVehicleUsers(user_id, vehicle_status):
    
    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
                '''
                    select vehicle_number from vehicles where user_id = (?) AND vehicle_status=(?)
                ''',(user_id,vehicle_status)
    )

    vehicles = cur.fetchall()
    connection.commit()
    connection.close()

    return vehicles

def insertReserveParkingSpot(spot_id, lot_id, user_id, vehicle_number):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    parking_timeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    

    cur.execute(
        '''
        INSERT INTO Reserve_Parking_Spot (
            spot_id,
            lot_id,
            user_id,
            vehicle_number,
            parking_timestamp,
            parking_cost
        ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (spot_id, lot_id, user_id, vehicle_number, parking_timeStamp, None)
    )

    connection.commit()
    connection.close()


def updateParkingSpotStatus(spot_id, lot_id, status):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute('''
                    UPDATE ParkingSpots 
                    SET status=(?) 
                    where spot_id=(?) AND lot_id = (?)
                ''',(status,spot_id,lot_id)
                )
    
    connection.commit()
    connection.close()

def getReserveParkingSpotData(user_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()
    print(user_id)
    cur.execute('''
                    select rp.spot_id,
                        pl.address AS location_name,
                        rp.vehicle_number,
                        rp.parking_timestamp,
                        ps.status,
                        pl.lot_id
                        from Reserve_Parking_Spot rp 
                    JOIN
                        ParkingLot pl on pl.lot_id = rp.lot_id 
                    JOIN 
                        ParkingSpots ps on rp.spot_id = ps.spot_id AND rp.lot_id = ps.lot_id
                    where 
                        rp.user_id = (?)
                ''',(user_id,)
                )
    
    result = cur.fetchall()

    connection.commit()
    connection.close()

    return result

def getPriceParkingLot(lot_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute('''
                    Select price from parkinglot where lot_id=(?)
                ''',(lot_id,))
    
    price = cur.fetchone()[0]

    connection.commit()
    connection.close()

    return price

def updateVehicleStatus(user_id, vehicle_number, vehicle_status):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute('''
        UPDATE Vehicles
        SET user_id = ?,
            vehicle_number = ?,
            vehicle_status = ?
        WHERE vehicle_number = ?;
    ''', (user_id, vehicle_number, vehicle_status, vehicle_number))

    # Check if any row was updated
    if cur.rowcount == 0:
        print(f"No vehicle found with vehicle_number: {vehicle_number}")
    else:
        print(f"Vehicle {vehicle_number} updated successfully.")
    
    connection.commit()
    connection.close()

def deleteReserveParkingSpot(user_id, vehicle_number):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute('''
                    DELETE FROM Reserve_Parking_Spot
                    WHERE vehicle_number = ?
                    AND user_id = ?;
                ''',(vehicle_number, user_id))
    
    connection.commit()
    connection.close()



