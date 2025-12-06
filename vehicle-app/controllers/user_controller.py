from flask import Blueprint, render_template, request, redirect, url_for, flash, session,jsonify
from models.users import create_user_table, register_user, check_user, fetch_user
from models.parking_lot import insertVehicleDetails, checkVehicleExists,get_availability_data, fetchOneParkingSpot, fetchVehicleUsers, insertReserveParkingSpot, updateParkingSpotStatus, getReserveParkingSpotData,getPriceParkingLot, updateVehicleStatus, deleteReserveParkingSpot
from flask_restx import Namespace, Resource
import bcrypt
import datetime

user = Blueprint('user',__name__)


auth_ns = Namespace('auth', description='Authentication API')


@user.route('/api/user/dashboard', methods=['GET'])
def user_dashboard_api():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Not authenticated"}), 401

    user_parking_data_tuples = getReserveParkingSpotData(user_id)
    availability_data_tuples = get_availability_data()

    # Convert tuples → objects
    user_parking_data = [{
        "reserve_id": p[0],
        "location": p[1],
        "vehicle_number": p[2],
        "parking_timestamp": p[3],
        "status": p[4],
        "lot_id": p[5]
    } for p in user_parking_data_tuples]

    availability_data = [{
        "lot_id": a[0],
        "location": a[1],
        "availability": a[2]
    } for a in availability_data_tuples]

    return jsonify({
        "success": True,
        "user_parking_data": user_parking_data,
        "availability_data": availability_data
    })


@user.route("/api/user/bookSpot", methods=['POST'])
def bookSpot_api():
    data = request.get_json()

    lot_id = data.get("lot_id")
    location_name = data.get("locationName")

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    # get the next available spot
    spot_id = fetchOneParkingSpot(lot_id)

    # Fetch user's registered vehicles
    vehicles_user = fetchVehicleUsers(user_id, 'F')

    if not vehicles_user:
        return jsonify({
            "success": False,
            "message": "No vehicles registered"
        })

    # Convert rows -> list of vehicle numbers
    vehicles_list = [v[0] for v in vehicles_user]

    return jsonify({
        "success": True,
        "lot_id": lot_id,
        "spot_id": spot_id[0],
        "user_id": user_id,
        "location_name": location_name,
        "vehicles": vehicles_list
    })



@user.route("/api/user/addVehicle", methods=['GET', 'POST'])
def addVehicle_api():

    if request.method == 'POST':
        data = request.get_json()

        user_id = session.get('user_id')
        vehicle_number = data.get("vehicle_number")

        if not user_id or not vehicle_number:
            return jsonify({"success": False, "message": "Please enter all the details"})

        if checkVehicleExists(vehicle_number):
            return jsonify({"success": False, "message": "Vehicle Number Already Exists"})

        insertVehicleDetails(user_id, vehicle_number, 'F')
        return jsonify({"success": True, "message": "Vehicle added successfully!"})

    # GET → return logged-in user info
    user_id = session.get('user_id')
    return jsonify({
        "success": True,
        "user_id": user_id
    })  


@user.route('/api/user/confirmBooking', methods=['POST'])
def confirmBooking_api():

    data = request.get_json()

    user_id = session.get('user_id')   
    locationName = data.get('locationName')
    lot_id = data.get('lot_id')
    spot_id = data.get('spot_id')
    vehicle_number = data.get('vehicle_number')

    #Converting Vehicle Number to Uppercase
    if vehicle_number:
        vehicle_number = vehicle_number.upper()

        # Validate Input
    if not (locationName and user_id and lot_id and spot_id and vehicle_number):
        return jsonify({
            "success": False,
            "message": "Missing required fields"
        }), 400

    #delete any parking reservation of same vehicle
    deleteReserveParkingSpot(user_id, vehicle_number)

    # Insert new reservation
    insertReserveParkingSpot(spot_id, lot_id, user_id, vehicle_number)

    # Update spot status to Occupied
    updateParkingSpotStatus(spot_id, lot_id, 'O')


    updateVehicleStatus(user_id, vehicle_number, 'P')

    return jsonify({
        "success": True,
        "message": "Booking Successful!"
    }), 200


@user.route("/api/user/releaseSpot", methods=["POST"])
def release_spot_api():

    data = request.get_json()

    spot_id = data.get("spot_id")
    vehicle_number = data.get("vehicle_number")
    lot_id = data.get("lot_id")
    parking_time = data.get("parking_time")

    if not (spot_id and vehicle_number and lot_id and parking_time):
        return jsonify({"success": False, "message": "Missing fields"}), 400

    release_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    price = getPriceParkingLot(lot_id)

    # Calculating Hours
    parking_dt = datetime.datetime.strptime(parking_time, "%Y-%m-%d %H:%M")
    release_dt = datetime.datetime.strptime(release_time, "%Y-%m-%d %H:%M")
    hours = int((release_dt - parking_dt).total_seconds() // 3600)

    total_cost = price + (hours * price)

    return jsonify({
        "success": True,
        "spot_id": spot_id,
        "vehicle_number": vehicle_number,
        "lot_id": lot_id,
        "parking_time": parking_time,
        "release_time": release_time,
        "total_cost": total_cost
    }), 200


@user.route("/api/user/confirmRelease", methods=["POST"])
def confirm_release_api():

    data = request.get_json()

    spot_id = data.get("spot_id")
    lot_id = data.get("lot_id")
    vehicle_number = data.get("vehicle_number")
    user_id = session.get("user_id")

    if not (spot_id and lot_id and vehicle_number):
        return jsonify({"success": False, "message": "Missing fields"}), 400

    updateParkingSpotStatus(spot_id, lot_id, 'A')
    updateVehicleStatus(user_id, vehicle_number, 'F')

    return jsonify({
        "success": True,
        "message": "Spot successfully released!"
    })

@user.route("/api/user/exportCSV", methods=["POST"])
def export_csv():
    user_id = session.get("user_id")
    user_name = session.get("user_name")

    if not user_id:
        return jsonify({"success": False, "message": "User not logged in"}), 401

    from tasks import export_user_csv
    export_user_csv.delay(user_id, user_name)

    return jsonify({"success": True, "message": "Your export has started. You will be notified once ready."})

