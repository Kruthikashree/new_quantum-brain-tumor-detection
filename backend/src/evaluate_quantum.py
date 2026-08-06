"""
evaluate_quantum.py

Evaluate Improved Hybrid Quantum Neural Network
"""

import numpy as np
import torch
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    ConfusionMatrixDisplay
)

from quantum_model import HybridQuantumClassifier

# --------------------------------------------------
# Device
# --------------------------------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Using Device:", device)

# --------------------------------------------------
# Load Test Data
# --------------------------------------------------

print("\nLoading Test Features...")

X_test = np.load("X_test_quantum.npy")
y_test = np.load("y_test_quantum.npy")

X_test = torch.tensor(
    X_test,
    dtype=torch.float32
).to(device)

# --------------------------------------------------
# Load Model
# --------------------------------------------------

model = HybridQuantumClassifier().to(device)

model.load_state_dict(
    torch.load(
        "quantum_model.pth",
        map_location=device
    )
)

model.eval()

print("Model Loaded Successfully!")

# --------------------------------------------------
# Prediction
# --------------------------------------------------

with torch.no_grad():

    outputs = model(X_test)

    probabilities = torch.softmax(outputs, dim=1)

    predictions = torch.argmax(
        probabilities,
        dim=1
    ).cpu().numpy()

# --------------------------------------------------
# Metrics
# --------------------------------------------------

accuracy = accuracy_score(
    y_test,
    predictions
)

precision = precision_score(
    y_test,
    predictions,
    average="weighted"
)

recall = recall_score(
    y_test,
    predictions,
    average="weighted"
)

f1 = f1_score(
    y_test,
    predictions,
    average="weighted"
)

print("\n==============================")
print("Hybrid Quantum Results")
print("==============================")

print(f"Accuracy  : {accuracy*100:.2f}%")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

# --------------------------------------------------
# Classification Report
# --------------------------------------------------

class_names = [
    "Glioma",
    "Meningioma",
    "No Tumor",
    "Pituitary"
]

print("\nClassification Report\n")

print(
    classification_report(
        y_test,
        predictions,
        target_names=class_names
    )
)

# --------------------------------------------------
# Confusion Matrix
# --------------------------------------------------

cm = confusion_matrix(
    y_test,
    predictions
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=class_names
)

fig, ax = plt.subplots(figsize=(8,8))

disp.plot(
    cmap="Blues",
    ax=ax,
    colorbar=False
)

plt.title("Hybrid Quantum Confusion Matrix")

plt.tight_layout()

plt.savefig(
    "quantum_confusion_matrix.png",
    dpi=300
)

plt.show()

print("\nConfusion Matrix Saved Successfully!")