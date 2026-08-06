import os

from flask import Blueprint
from flask import request
from flask import jsonify

from services.predictor import predict_image

prediction_bp = Blueprint("prediction", __name__)

UPLOAD_FOLDER = "uploads"

@prediction_bp.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:

        return jsonify({
            "error": "No image uploaded"
        }), 400

    file = request.files["image"]

    if file.filename == "":

        return jsonify({
            "error": "Empty filename"
        }), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(filepath)

    result = predict_image(filepath)

    return jsonify(result)