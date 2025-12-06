from flask import Blueprint, render_template, request, redirect, url_for, flash, session,jsonify
from models.users import create_user_table, register_user, check_user, fetch_user
import bcrypt

auth = Blueprint('auth',__name__)

create_user_table()

@auth.route('/api/register', methods=['POST'])
def register_api():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    fullname = data.get("fullname")
    address = data.get("address")
    pincode = data.get("pincode")
    phone_no = data.get("phone_no")

    # Validate email exists
    if check_user(email):
        return jsonify({
            "success": False,
            "message": "Email already exists"
        }), 400

    # Hash password
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Validate fields
    if not all([email, password, fullname, address, pincode, phone_no]):
        return jsonify({
            "success": False,
            "message": "Please fill all fields"
        }), 400

    register_user(email, hashed_pw, fullname, address, pincode, phone_no)

    return jsonify({
        "success": True,
        "message": "Registration successful"
    }), 201


@auth.route('/api/login', methods=['POST'])
def login_api():

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = fetch_user(email, password)
    print("Fetched user:", user)

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid credentials"
        }), 401

    # Set session (optional if you want login persistence)
    session['user_id'] = user[0]
    session['user'] = email
    session['role'] = user[-1]
    session['name'] = user[3]

    return jsonify({
        "success": True,
        "user_id": user[0],
        "email": email,
        "name": user[3],
        "role": user[-1]
    }), 200
 

# @auth.route('/admin/dashboard',methods=['GET','POST'])
# def admin_dashboard():

#     return render_template("dashboard/admin_dashboard.html")


# @auth.route('/logout', methods=['GET','POST'])
# def logout():

#     session.pop('user',None)
#     flash("You have been logged out")
#     return redirect(url_for('auth.login'))







