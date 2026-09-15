import os
import random
import string

from flask import Blueprint, request, jsonify
from database.mongodb import patients
from services.explainer import explain_image

patient_bp = Blueprint("patient", __name__)

UPLOAD_FOLDER = "uploads"


def generate_access_code():
    while True:
        code = "".join(random.choices(string.digits, k=6))
        if patients.find_one({"access_code": code}) is None:
            return code


@patient_bp.route("/patients", methods=["POST"])
def create_patient():

    patient_name = request.form.get("patient_name")
    patient_age = request.form.get("patient_age")
    patient_gender = request.form.get("patient_gender")
    lab_notes = request.form.get("lab_notes", "")

    if not patient_name or not patient_age or not patient_gender:
        return jsonify({"error": "Patient name, age, and gender are required"}), 400

    if "image" not in request.files:
        return jsonify({"error": "No MRI image uploaded"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    access_code = generate_access_code()

    filename = f"{access_code}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    file.save(filepath)

    patients.insert_one({
        "access_code": access_code,
        "patient_name": patient_name,
        "patient_age": patient_age,
        "patient_gender": patient_gender,
        "lab_notes": lab_notes,
        "image_path": filepath,
        "status": "pending",
        "result": None
    })

    return jsonify({
        "message": "Patient record created successfully",
        "access_code": access_code
    })


@patient_bp.route("/patients/code/<access_code>", methods=["GET"])
def get_patient_by_code(access_code):

    record = patients.find_one({"access_code": access_code})

    if record is None:
        return jsonify({"error": "No patient found for this access code"}), 404

    return jsonify({
        "access_code": record["access_code"],
        "patient_name": record["patient_name"],
        "patient_age": record["patient_age"],
        "patient_gender": record["patient_gender"],
        "lab_notes": record.get("lab_notes", ""),
        "status": record["status"],
        "result": record.get("result")
    })


@patient_bp.route("/patients/code/<access_code>/generate-result", methods=["POST"])
def generate_result(access_code):

    record = patients.find_one({"access_code": access_code})

    if record is None:
        return jsonify({"error": "No patient found for this access code"}), 404

    if record["status"] == "analyzed" and record.get("result"):
        return jsonify({
            "message": "Result already generated",
            "result": record["result"]
        })

    result = explain_image(record["image_path"])

    patients.update_one(
        {"access_code": access_code},
        {"$set": {"status": "analyzed", "result": result}}
    )

    return jsonify({
        "message": "Result generated successfully",
        "result": result
    })


@patient_bp.route("/patients", methods=["GET"])
def list_patients():

    records = list(patients.find({}, {
        "access_code": 1,
        "patient_name": 1,
        "patient_age": 1,
        "patient_gender": 1,
        "status": 1,
        "result": 1,
        "_id": 0
    }).sort("_id", -1))

    return jsonify(records)
