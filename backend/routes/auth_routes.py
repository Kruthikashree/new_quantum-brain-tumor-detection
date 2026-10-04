from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from database.mongodb import users, pending_signups, otps
from services.otp_service import create_and_send_otp, verify_otp
from services.token_service import create_token
import bcrypt

auth_bp = Blueprint("auth", __name__)


def clean_email(value):
    return (value or "").strip().lower()


# -------------------------------
# Signup: step 1 (send code)
# -------------------------------
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}

    name = (data.get("name") or "").strip()
    email = clean_email(data.get("email"))
    password = data.get("password") or ""
    role = data.get("role")  # "lab" or "doctor"

    if not name or not email or not password or not role:
        return jsonify({"error": "All fields are required"}), 400

    if role not in ("lab", "doctor"):
        return jsonify({"error": "Role must be 'lab' or 'doctor'"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    if users.find_one({"email": email}):
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Keep the details in a temporary record until the email is verified
    pending_signups.delete_many({"email": email})
    pending_signups.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": role,
        "expires_at": datetime.utcnow() + timedelta(minutes=10),
    })

    try:
        create_and_send_otp(otps, email)
    except Exception as e:
        print("Email error:", e)
        pending_signups.delete_many({"email": email})
        return jsonify({"error": "Could not send verification email"}), 500

    return jsonify({
        "message": "Verification code sent",
        "email": email,
    })


# -------------------------------
# Signup: step 2 (check code, create account)
# -------------------------------
@auth_bp.route("/verify-signup", methods=["POST"])
def verify_signup():
    data = request.get_json() or {}
    email = clean_email(data.get("email"))
    code = str(data.get("code") or "").strip()

    if not email or not code:
        return jsonify({"error": "Email and code are required"}), 400

    pending = pending_signups.find_one({"email": email})
    if not pending:
        return jsonify({"error": "Signup expired. Please sign up again."}), 400

    ok, message = verify_otp(otps, email, code)
    if not ok:
        return jsonify({"error": message}), 400

    if users.find_one({"email": email}):
        pending_signups.delete_many({"email": email})
        return jsonify({"error": "Email already exists"}), 400

    users.insert_one({
        "name": pending["name"],
        "email": email,
        "password": pending["password"],
        "role": pending["role"],
        "verified": True,
    })
    pending_signups.delete_many({"email": email})

    return jsonify({"message": "Account Created Successfully"})


# -------------------------------
# Resend the code
# -------------------------------
@auth_bp.route("/resend-code", methods=["POST"])
def resend_code():
    data = request.get_json() or {}
    email = clean_email(data.get("email"))

    pending = pending_signups.find_one({"email": email})
    if not pending:
        return jsonify({"error": "Signup expired. Please sign up again."}), 400

    pending_signups.update_one(
        {"email": email},
        {"$set": {"expires_at": datetime.utcnow() + timedelta(minutes=10)}},
    )

    try:
        create_and_send_otp(otps, email)
    except Exception as e:
        print("Email error:", e)
        return jsonify({"error": "Could not send verification email"}), 500

    return jsonify({"message": "New code sent"})


# -------------------------------
# Login (now returns a signed token)
# -------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = clean_email(data.get("email"))
    password = data.get("password") or ""

    user = users.find_one({"email": email})

    if user is None:
        return jsonify({"error": "Invalid Email"}), 401

    if bcrypt.checkpw(password.encode(), user["password"]):
        return jsonify({
            "message": "Login Successful",
            "name": user["name"],
            "email": user["email"],
            "role": user.get("role", "lab"),
            "token": create_token(user),
        })

    return jsonify({"error": "Wrong Password"}), 401

# -------------------------------
# Forgot password: step 1 (send code)
# -------------------------------
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json() or {}
    email = clean_email(data.get("email"))

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = users.find_one({"email": email})
    # Always return the same message, whether or not the account exists,
    # so this endpoint can't be used to check which emails are registered.
    if user is not None:
        try:
            create_and_send_otp(otps, email)
        except Exception as e:
            print("Email error:", e)

    return jsonify({
        "message": "If an account exists for this email, a reset code has been sent."
    })


# -------------------------------
# Forgot password: step 2 (check code, set new password)
# -------------------------------
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json() or {}
    email = clean_email(data.get("email"))
    code = str(data.get("code") or "").strip()
    new_password = data.get("new_password") or ""

    if not email or not code or not new_password:
        return jsonify({"error": "Email, code and new password are required"}), 400

    if len(new_password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    user = users.find_one({"email": email})
    if user is None:
        return jsonify({"error": "Invalid or expired code"}), 400

    ok, message = verify_otp(otps, email, code)
    if not ok:
        return jsonify({"error": message}), 400

    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    users.update_one({"email": email}, {"$set": {"password": hashed}})

    return jsonify({"message": "Password reset successfully"})