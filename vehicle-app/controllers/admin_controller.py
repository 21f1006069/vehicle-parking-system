import sqlite3
from config import DATABASE_PARKING
from flask import Blueprint, render_template, request, redirect, url_for, flash, session,jsonify
from models.parking_lot import insertParkingLot,createParkingSpots, insertParkingSpots, get_all_parking_lots, get_all_parking_spots, fetch_parking_lot, updateParkinglot, deleteParkingLotAndSpot, deleteParticularParkingSpot, getUsersData

admin = Blueprint('admin',__name__)

@admin.route("/api/admin/dashboard", methods = ['GET','POST'])
def admin_dashboard_api():

    def getOccupiedValue(spots):
        occupied = 0
        for s in spots:
            if s[2] == 'O': 
                occupied = occupied+1 

        return occupied
    
    lots = get_all_parking_lots()
    print(lots)

    all_parking_lots = []
    
    for lot in lots:
        # Assuming lot is a tuple and the first element is the id
        # lot_id = lot[0]
        # spots = get_all_parking_spots(lot_id)
        # total = len(spots)   
        # occupied = getOccupiedValue(spots)
        # available = total - occupied

        # all_parking_lots.append({
        #     "lot": lot,
        #     "spots": spots,
        #     "total": total,
        #     "occupied": occupied,
        #     "available": available,
        # })

        lot_id = lot[0]

        spots = get_all_parking_spots(lot_id)  # list of tuples

        spots_clean = [
            {
                "spot_id": s[1],
                "lot_id": s[0],
                "status": s[2]
            }
            for s in spots
        ]

        # Create clean lot object
        lot_clean = {
            "lot_id": lot[0],
            "location_name": lot[1],
            "address": lot[2],
            "pincode": lot[3],
            "price": lot[4],
            "maxSpots": lot[5],
            "total": len(spots),
            "occupied": getOccupiedValue(spots),
            "available": len(spots) - getOccupiedValue(spots),
            "spots": spots_clean
        }

        all_parking_lots.append(lot_clean)


    print(all_parking_lots)

    #return render_template("dashboard/admin_dashboard.html", lots_data = all_parking_lots)

    return jsonify({
        "success": True,
        "lots": all_parking_lots
    })


@admin.route('/api/admin/lot/add', methods=['POST'])
def add_lot_api():

    data = request.get_json()

    locationName = data.get('locationName')
    address = data.get('address')
    pincode = data.get('pincode')
    pricePerHour = data.get('pricePerHour')
    maxSpots = data.get('maxSpots')

    # Validate fields
    if not locationName or not address or not pincode or not pricePerHour or not maxSpots:
        return jsonify({
            "success": False,
            "message": "Please enter all the details"
        }), 400

    # Insert lot
    lot_id = insertParkingLot(locationName, address, pincode, pricePerHour, maxSpots)
    maxSpots = int(maxSpots)

    # Create parking spots
    for i in range(1, maxSpots + 1):
        insertParkingSpots(lot_id, i)

    return jsonify({
        "success": True,
        "message": "Parking Lot added successfully",
        "lot_id": lot_id
    }), 200
            
    #return render_template('admin/addlot.html')

@admin.route('/api/admin/lot/<int:lot_id>', methods=['GET'])
def get_lot(lot_id):
    parking_lot_data = fetch_parking_lot(lot_id)

    if not parking_lot_data:
        return jsonify({"success": False, "message": "Lot not found"}), 404

    return jsonify({
        "success": True,
        "lot": {
            "lot_id": parking_lot_data[0],
            "location_name": parking_lot_data[1],
            "address": parking_lot_data[2],
            "pincode": parking_lot_data[3],
            "price": parking_lot_data[4],
            "maxSpots": parking_lot_data[5]
        }
    }), 200


@admin.route('/api/admin/lot/update', methods=['POST'])
def update_lot():
    data = request.get_json()

    required = ["locationName", "address", "pincode", "pricePerHour", "maxSpots", "lot_id"]
    for r in required:
        if not data.get(r):
            return jsonify({"success": False, "message": f"Missing field: {r}"}), 400

    updateParkinglot(
        data["locationName"],
        data["address"],
        data["pincode"],
        data["pricePerHour"],
        data["maxSpots"],
        int(data["lot_id"])
    )

    return jsonify({
        "success": True,
        "message": "Parking lot updated successfully"
    }), 200


@admin.route('/api/admin/lot/delete/<int:lot_id>', methods=['POST'])
def api_delete_lot(lot_id):

    parkinglotdata = fetch_parking_lot(lot_id)
    if not parkinglotdata:
        return jsonify({
            "success": False,
            "message": "Parking lot not found"
        }), 404

    deleteParkingLotAndSpot(lot_id)

    return jsonify({
        "success": True,
        "message": "Parking lot deleted successfully"
    }), 200

@admin.route('/api/admin/spot/<int:lot_id>/<int:spot_id>/<string:status>', methods=['GET'])
def api_view_spot(lot_id, spot_id, status):

    if spot_id is None or lot_id is None or status is None:
        return jsonify({
            "success": False,
            "message": "Invalid Lot ID or Spot ID"
        }), 400

    return jsonify({
        "success": True,
        "spot": {
            "spot_id": spot_id,
            "lot_id": lot_id,
            "status": status
        }
    }), 200

@admin.route('/api/admin/spot/delete', methods=['POST'])
def api_delete_spot():
    data = request.get_json()

    spot_id = data.get('spot_id')
    lot_id = data.get('lot_id')

    if not spot_id or not lot_id:
        return jsonify({
            "success": False,
            "message": "Missing spot_id or lot_id"
        }), 400

    deleteParticularParkingSpot(spot_id, lot_id)

    return jsonify({
        "success": True,
        "message": "Spot deleted successfully"
    }), 200


@admin.route('/api/admin/users', methods=['GET'])
def api_users():
    users = getUsersData()

    clean_users = []
    for u in users:
        clean_users.append({
            "id": u[0],
            "email": u[1],
            "fullname": u[3],
            "address": u[4],
            "pincode": u[5]
        })

    return jsonify({
        "success": True,
        "users": clean_users
    }), 200


@admin.route('/api/admin/summary', methods=['GET'])
def api_admin_summary():
    conn = sqlite3.connect(DATABASE_PARKING)
    cursor = conn.cursor()

    # Total lots
    cursor.execute("SELECT COUNT(*) FROM ParkingLot")
    total_lots = cursor.fetchone()[0]

    # Total spots
    cursor.execute("SELECT COUNT(*) FROM ParkingSpots")
    total_spots = cursor.fetchone()[0]

    # Count of spots by status
    cursor.execute("SELECT status, COUNT(*) FROM ParkingSpots GROUP BY status")
    status_data = cursor.fetchall()
    status_summary = {item[0]: item[1] for item in status_data}

    # Count of spots per lot
    cursor.execute("SELECT lot_id, COUNT(*) FROM ParkingSpots GROUP BY lot_id")
    lot_spot_data = cursor.fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "total_lots": total_lots,
        "total_spots": total_spots,
        "status_summary": status_summary,
        "lot_spot_data": lot_spot_data
    }), 200



    

    
