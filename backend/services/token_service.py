import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import request, jsonify, g

TOKEN_HOURS = 8


def _secret():
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET is not set in .env")
    return secret


def create_token(user):
    payload = {
        "sub": str(user["_id"]),
        "email": user["email"],
        "name": user["name"],
        "role": user.get("role", "lab"),
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_HOURS),
    }
    return jwt.encode(payload, _secret(), algorithm="HS256")


def require_auth(*roles):
    """Use as @require_auth("doctor") or @require_auth("lab", "doctor")."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization", "")
            if not header.startswith("Bearer "):
                return jsonify({"error": "Login required"}), 401
            try:
                claims = jwt.decode(header[7:], _secret(), algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Session expired. Please log in again."}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid session"}), 401
            if roles and claims.get("role") not in roles:
                return jsonify({"error": "You are not authorized to do this"}), 403
            g.user = claims
            return fn(*args, **kwargs)
        return wrapper
    return decorator