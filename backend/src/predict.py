"""
predict.py

Predict Brain Tumor using Improved Hybrid Quantum Neural Network
"""

import os
import numpy as np
import torch
import joblib

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from quantum_model import HybridQuantumClassifier

# --------------------------------------------------
# Configuration
# --------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SCALER_PATH = os.path.join(CURRENT_DIR, "scaler.pkl")
MODEL_PATH = os.path.join(CURRENT_DIR, "quantum_model.pth")

IMG_SIZE = 224

CLASS_NAMES = [
    "Glioma",
    "Meningioma",
    "No Tumor",
    "Pituitary"
]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --------------------------------------------------
# MobileNet Feature Extractor
# --------------------------------------------------

feature_extractor = MobileNetV2(
    weights="imagenet",
    include_top=False,
    pooling="avg",
    input_shape=(224,224,3)
)

# --------------------------------------------------
# Load StandardScaler
# --------------------------------------------------

scaler = joblib.load(SCALER_PATH)

# --------------------------------------------------
# Load Hybrid Model
# --------------------------------------------------

model = HybridQuantumClassifier().to(device)

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)

model.eval()

# --------------------------------------------------
# Prediction Function
# --------------------------------------------------

def predict(image_path):

    img = image.load_img(
        image_path,
        target_size=(IMG_SIZE, IMG_SIZE)
    )

    img = image.img_to_array(img)

    img = np.expand_dims(img, axis=0)

    img = preprocess_input(img)

    features = feature_extractor.predict(
        img,
        verbose=0
    )

    features = scaler.transform(features)

    features = torch.tensor(
        features,
        dtype=torch.float32
    ).to(device)

    with torch.no_grad():

        output = model(features)

        probabilities = torch.softmax(
            output,
            dim=1
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1
        )

    return (
        CLASS_NAMES[prediction.item()],
        confidence.item() * 100
    )

# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    image_path = input("Enter MRI Image Path : ")

    tumor, confidence = predict(image_path)

    print("\n==============================")
    print("Prediction Result")
    print("==============================")
    print(f"Tumor Type : {tumor}")
    print(f"Confidence : {confidence:.2f}%")
