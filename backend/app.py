import os

from flask import Flask
from flask_cors import CORS


from routes.auth_routes import auth_bp

from routes.report_routes import report_bp

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB uploads

CORS(app)


app.register_blueprint(auth_bp)

app.register_blueprint(report_bp)


@app.route("/")
def home():
    return {"message": "Quantum Brain Tumor Detection API Running"}


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG") == "1",
        use_reloader=False,
        host="127.0.0.1",
        port=5000,
    )