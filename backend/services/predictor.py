import os
import sys

# Add src folder to path
CURRENT_DIR = os.path.dirname(__file__)
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))

if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from predict import predict


def predict_image(image_path):
    """
    Calls your existing hybrid quantum model.
    """
    tumor, confidence = predict(image_path)

    return {
        "tumor": tumor,
        "confidence": round(confidence, 2)
    }