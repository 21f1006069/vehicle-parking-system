from flask import Flask, session, jsonify
from flask_cors import CORS
from controllers.auth_controller import auth
from controllers.admin_controller import admin
from controllers.user_controller import user
from models.parking_lot import createParkingLot, createParkingSpots, createReserveParkingSpot, createVehiclesTable
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os
import uuid


load_dotenv()

# ---------------------------
# Create Flask App
# ---------------------------
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.getenv("SECRET_KEY")

#Blueprints
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)

#Create Tables
createParkingLot()
createParkingSpots()
createReserveParkingSpot()
createVehiclesTable()


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
