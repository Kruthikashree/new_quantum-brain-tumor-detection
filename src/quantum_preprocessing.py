"""
quantum_preprocessing.py

Quantum preprocessing without PCA

Input:
    X_train.npy
    X_test.npy

Output:
    X_train_quantum.npy
    X_test_quantum.npy
"""

import numpy as np
import joblib

from sklearn.preprocessing import StandardScaler

print("="*50)
print("Quantum Preprocessing Started")
print("="*50)

# --------------------------------------------------
# Load MobileNet Features
# --------------------------------------------------

X_train = np.load("X_train.npy")
X_test = np.load("X_test.npy")

y_train = np.load("y_train.npy")
y_test = np.load("y_test.npy")

print("\nOriginal Shapes")

print("Train :", X_train.shape)
print("Test  :", X_test.shape)

# --------------------------------------------------
# StandardScaler
# --------------------------------------------------

print("\nApplying StandardScaler...")

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

# --------------------------------------------------
# Save
# --------------------------------------------------

np.save("X_train_quantum.npy", X_train)
np.save("X_test_quantum.npy", X_test)

np.save("y_train_quantum.npy", y_train)
np.save("y_test_quantum.npy", y_test)

joblib.dump(
    scaler,
    "scaler.pkl"
)

print("\nSaved Successfully!")

print("\nQuantum Feature Shape")

print("Train :", X_train.shape)
print("Test  :", X_test.shape)

print("\nDone.")