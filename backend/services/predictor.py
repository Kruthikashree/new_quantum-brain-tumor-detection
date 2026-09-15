import os
import sys

# Add src folder to path (robust: computed relative to this file's location)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


def predict_image(image_path):
    """
    Calls the hybrid quantum model.
    Import is done lazily (inside the function) so that any import-path
    issues surface with a clear error instead of crashing app startup.
    """
    from predict import predict

    tumor, confidence = predict(image_path)

    return {
        "tumor": tumor,
        "confidence": round(confidence, 2)
    }
