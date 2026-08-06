from flask import Blueprint, request, jsonify
from database.mongodb import users
import bcrypt

auth_bp = Blueprint("auth", __name__)


# -------------------------------
# Signup
# -------------------------------
@auth_bp.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    existing = users.find_one({"email": email})

    if existing:
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    users.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password
    })

    return jsonify({
        "message": "Account Created Successfully"
    })


# -------------------------------
# Login
# -------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = users.find_one({
        "email": email
    })

    if user is None:
        return jsonify({
            "error": "Invalid Email"
        }), 401

    if bcrypt.checkpw(
        password.encode(),
        user["password"]
    ):

        return jsonify({
            "message": "Login Successful",
            "name": user["name"]
        })

    return jsonify({
        "error": "Wrong Password"
    }), 401