import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


def explain_image(image_path):
    from quantum_explain import generate_explanation
    return generate_explanation(image_path)
