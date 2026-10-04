import os, hmac, hashlib, random
from datetime import datetime, timedelta
from services.email_service import send_email

OTP_MINUTES = 10
MAX_ATTEMPTS = 5


def _now():
    return datetime.utcnow()


def _hash(code):
    secret = os.getenv("OTP_SECRET", "change-me")
    return hashlib.sha256((code + secret).encode()).hexdigest()


def create_and_send_otp(otps, email):
    """otps = the MongoDB collection that stores codes."""
    code = f"{random.SystemRandom().randint(0, 999999):06d}"
    otps.delete_many({"email": email})
    otps.insert_one({
        "email": email,
        "code_hash": _hash(code),
        "expires_at": _now() + timedelta(minutes=OTP_MINUTES),
        "attempts": 0,
    })
    send_email(
        email,
        "Your verification code",
        f"Your verification code is {code}.\n"
        f"It expires in {OTP_MINUTES} minutes. If you didn't sign up, ignore this email.",
    )


def verify_otp(otps, email, code):
    """Returns (ok: bool, message: str)."""
    rec = otps.find_one({"email": email})
    if not rec:
        return False, "No code found. Please request a new one."
    if rec["attempts"] >= MAX_ATTEMPTS:
        return False, "Too many wrong attempts. Please request a new code."
    if _now() > rec["expires_at"]:
        return False, "Code expired. Please request a new one."
    if hmac.compare_digest(_hash(code.strip()), rec["code_hash"]):
        otps.delete_many({"email": email})
        return True, "Verified."
    otps.update_one({"email": email}, {"$inc": {"attempts": 1}})
    return False, "Incorrect code."