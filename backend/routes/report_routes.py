import base64
import io
import os
import re
import time
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from datetime import timedelta
from bson import ObjectId
from bson.errors import InvalidId
from flask import Blueprint, request, jsonify, g, send_file
from PIL import Image
from werkzeug.utils import secure_filename

from database.mongodb import reports
from services.token_service import require_auth
from services.referral_service import insert_with_unique_code
from services.explainer import explain_image
from services.report_service import build_pdf, send_report_emails
from services.image_validator import looks_like_mri

report_bp = Blueprint("reports", __name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "reports")
ALLOWED_EXT = {".png", ".jpg", ".jpeg"}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

REQUIRED = {
    "patient_name": "Patient full name",
    "patient_id": "Patient ID",
    "patient_age": "Age",
    "patient_gender": "Gender",
    "patient_email": "Patient email",
    "patient_phone": "Patient phone number",
    "preferred_language": "Preferred language",
    "doctor_name": "Doctor full name",
    "doctor_email": "Doctor email",
    "hospital": "Hospital/Clinic name",
    "scan_date": "Scan date",
}

_failed = defaultdict(list)
MAX_FAILED = 10
WINDOW_SECONDS = 600


def _too_many_failures(user_id):
    now = time.time()
    _failed[user_id] = [t for t in _failed[user_id] if now - t < WINDOW_SECONDS]
    return len(_failed[user_id]) >= MAX_FAILED


def _load(report_id):
    try:
        return reports.find_one({"_id": ObjectId(report_id)})
    except (InvalidId, TypeError):
        return None


def _is_assigned(report):
    user = g.user
    if user["role"] == "lab":
        return report.get("lab_id") == user["sub"]
    if user["role"] == "doctor":
        return report["doctor"]["email"] == user["email"]
    return False


def _can_access(report):
    """Lab: owns it. Doctor: assigned AND has unlocked it with the referral code."""
    user = g.user
    if user["role"] == "lab":
        return report.get("lab_id") == user["sub"]
    if user["role"] == "doctor":
        is_unlocked = user["email"] in (report.get("unlocked_by") or [])
        return _is_assigned(report) and is_unlocked
    return False


def _image_data_url(path):
    try:
        ext = os.path.splitext(path)[1].lower().lstrip(".")
        mime = "image/png" if ext == "png" else "image/jpeg"
        with open(path, "rb") as f:
            return f"data:{mime};base64," + base64.b64encode(f.read()).decode()
    except Exception:
        return None


def serialize(r, detail=False):
    """Everyone who can access a report (lab owner, or a doctor who has
    unlocked it) now sees the AI result — results are generated at
    creation time, not withheld by role."""
    result = r.get("result") or {}
    out = {
        "id": str(r["_id"]),
        "referral_code": r["referral_code"],
        "patient": r["patient"],
        "doctor": r["doctor"],
        "lab_name": r["lab_name"],
        "scan_date": r["scan_date"],
        "created_at": r["created_at"].isoformat(),
        "email_status": r.get("email_status"),
        "status": r.get("status", "pending"),
                "result": {
            "tumor": result.get("tumor"),
            "confidence": result.get("confidence"),
            "probabilities": result.get("probabilities"),
        } if result else None,
    }

    if detail:
        out["clinical_notes"] = r.get("clinical_notes", "")
        out["mri_image"] = _image_data_url(r["image_path"])
        if result:
            out["result"]["heatmap"] = result.get("heatmap")

    return out


# ------------------------------------------------------------
# Lab: create a report AND run the AI analysis immediately
# ------------------------------------------------------------
@report_bp.route("/reports", methods=["POST"])
@require_auth("lab")
def create_report():
    form = request.form

    def val(key):
        return (form.get(key) or "").strip()

    missing = [label for key, label in REQUIRED.items() if not val(key)]
    if missing:
        return jsonify({"error": "Missing: " + ", ".join(missing)}), 400

    if form.get("consent") != "true":
        return jsonify({"error": "Patient consent is required"}), 400

    patient_email = val("patient_email").lower()
    doctor_email = val("doctor_email").lower()
    if not EMAIL_RE.match(patient_email) or not EMAIL_RE.match(doctor_email):
        return jsonify({"error": "Enter valid email addresses"}), 400

    try:
        age = int(val("patient_age"))
        if not 0 <= age <= 120:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Enter a valid age"}), 400

    try:
        scan_dt = datetime.strptime(val("scan_date"), "%Y-%m-%dT%H:%M")
        if scan_dt > datetime.now():
            raise ValueError
    except ValueError:
        return jsonify({"error": "Enter a valid scan date and time (not in the future)"}), 400

    file = request.files.get("image")
    if not file or not file.filename:
        return jsonify({"error": "MRI image is required"}), 400
    ext = os.path.splitext(secure_filename(file.filename))[1].lower()
    if ext not in ALLOWED_EXT:
        return jsonify({"error": "MRI image must be PNG or JPG"}), 400

    try:
        pil_img = Image.open(file.stream)
        pil_img.load()
    except Exception:
        return jsonify({"error": "The uploaded file is not a valid image"}), 400

    ok, reason = looks_like_mri(pil_img)
    if not ok:
        return jsonify({"error": reason}), 400

    file.stream.seek(0)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    image_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}{ext}")
    file.save(image_path)

    # Run the AI pipeline right now, as part of report creation
    try:
        result = explain_image(image_path)
    except Exception as e:
        print("AI analysis error:", e)
        os.remove(image_path)
        return jsonify({"error": "AI analysis failed. Please try again."}), 500

    doc = {
        "lab_id": g.user["sub"],
        "lab_name": g.user["name"],
        "patient": {
            "full_name": val("patient_name"),
            "patient_id": val("patient_id"),
            "age": age,
            "gender": val("patient_gender"),
            "email": patient_email,
            "phone": val("patient_phone"),
            "language": val("preferred_language"),
        },
        "doctor": {
            "full_name": val("doctor_name"),
            "email": doctor_email,
            "hospital": val("hospital"),
            "doctor_id": val("doctor_id"),
        },
        "scan_date": val("scan_date"),
        "clinical_notes": val("clinical_notes"),
        "image_path": image_path,
        "result": result,
        "status": "analyzed",
        "analyzed_at": datetime.now(timezone.utc),
        "analyzed_by": g.user["email"],
        "consent": {"given": True, "at": datetime.now(timezone.utc)},
        "created_at": datetime.now(timezone.utc),
        "email_status": {"doctor": False, "patient": False},
    }

    try:
        report_id = insert_with_unique_code(reports, doc)
    except Exception as e:
        print("Insert error:", e)
        os.remove(image_path)
        return jsonify({"error": "Could not save the report"}), 500

    status = send_report_emails(doc)
    reports.update_one({"_id": report_id}, {"$set": {"email_status": status}})
    doc["email_status"] = status

    return jsonify({"message": "Report generated", "report": serialize(doc, detail=True)})


# ------------------------------------------------------------
# Lab / Doctor: history
# ------------------------------------------------------------
@report_bp.route("/reports", methods=["GET"])
@require_auth("lab", "doctor")
def list_reports():
    is_lab = g.user["role"] == "lab"
    if is_lab:
        query = {"lab_id": g.user["sub"]}
    else:
        query = {"doctor.email": g.user["email"], "unlocked_by": g.user["email"]}
    rows = reports.find(query).sort("created_at", -1).limit(200)
    return jsonify([serialize(r) for r in rows])


# ------------------------------------------------------------
# Lab / Doctor: one report (owner, or a doctor who has unlocked it)
# ------------------------------------------------------------
@report_bp.route("/reports/<report_id>", methods=["GET"])
@require_auth("lab", "doctor")
def get_report(report_id):
    report = _load(report_id)
    if report is None:
        return jsonify({"error": "Report not found"}), 404
    if not _can_access(report):
        return jsonify({"error": "You are not authorized to access this report."}), 403
    return jsonify(serialize(report, detail=True))


# ------------------------------------------------------------
# Doctor: unlock a report with a referral code
# ------------------------------------------------------------
@report_bp.route("/reports/lookup", methods=["POST"])
@require_auth("doctor")
def lookup_report():
    user_id = g.user["sub"]
    if _too_many_failures(user_id):
        return jsonify({"error": "Too many attempts. Please try again in a few minutes."}), 429

    code = str((request.get_json() or {}).get("code") or "").strip()
    report = reports.find_one({"referral_code": code}) if re.fullmatch(r"\d{6}", code) else None

    if report is None:
        _failed[user_id].append(time.time())
        return jsonify({"error": "Invalid referral code."}), 404

    if not _is_assigned(report):
        _failed[user_id].append(time.time())
        return jsonify({"error": "You are not authorized to access this report."}), 403

    reports.update_one(
        {"_id": report["_id"], "first_viewed_at": {"$exists": False}},
        {"$set": {"first_viewed_at": datetime.now(timezone.utc)}},
    )
    reports.update_one(
        {"_id": report["_id"]},
        {"$addToSet": {"unlocked_by": g.user["email"]}},
    )
    report = reports.find_one({"_id": report["_id"]})
    return jsonify(serialize(report, detail=True))


# ------------------------------------------------------------
# Lab / Doctor: PDF download (full report, including the AI section)
# ------------------------------------------------------------
@report_bp.route("/reports/<report_id>/pdf", methods=["GET"])
@require_auth("lab", "doctor")
def report_pdf(report_id):
    report = _load(report_id)
    if report is None:
        return jsonify({"error": "Report not found"}), 404
    if not _can_access(report):
        return jsonify({"error": "You are not authorized to access this report."}), 403
    pdf = build_pdf(report, include_result=True)
    return send_file(
        io.BytesIO(pdf),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"MRI_Report_{report['referral_code']}.pdf",
    )
from datetime import timedelta

@report_bp.route("/reports/stats", methods=["GET"])
@require_auth("lab")
def report_stats():
    lab_reports = list(reports.find({"lab_id": g.user["sub"]}))

    total = len(lab_reports)
    week_ago = datetime.now() - timedelta(days=7)
    last_7_days = sum(1 for r in lab_reports if r["created_at"] >= week_ago)
    pending_email = sum(
        1 for r in lab_reports
        if not (r.get("email_status", {}).get("doctor") and r.get("email_status", {}).get("patient"))
    )

    distribution = {"Glioma": 0, "Meningioma": 0, "Pituitary": 0, "No Tumor": 0}
    for r in lab_reports:
        tumor = (r.get("result") or {}).get("tumor")
        if tumor in distribution:
            distribution[tumor] += 1

    daily = {}
    for i in range(6, -1, -1):
        day = (datetime.now() - timedelta(days=i)).date().isoformat()
        daily[day] = 0
    for r in lab_reports:
        day = r["created_at"].date().isoformat()
        if day in daily:
            daily[day] += 1

    return jsonify({
        "total": total,
        "last_7_days": last_7_days,
        "pending_email": pending_email,
        "distribution": distribution,
        "weekly": [{"date": d, "count": c} for d, c in daily.items()],
    })