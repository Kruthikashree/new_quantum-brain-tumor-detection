from flask import Flask
from flask_cors import CORS

from routes.prediction_routes import prediction_bp
from routes.auth_routes import auth_bp
from routes.patient_routes import patient_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(prediction_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(patient_bp)


@app.route("/")
def home():

    return {
        "message": "Quantum Brain Tumor Detection API Running"
    }


if __name__ == "__main__":

    app.run(
        debug=True,
        use_reloader=False,
        host="0.0.0.0",
        port=5000
    )
