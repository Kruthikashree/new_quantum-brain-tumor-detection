"""
plot_quantum_vs_classical.py

Trains a FRESH, THROWAWAY copy of the Hybrid Quantum model (same
architecture/hyperparameters as train_quantum.py) purely to capture
epoch-by-epoch validation accuracy for comparison against the
MobileNetV2 (classical) curve already saved by
plot_training_curves.py.

IMPORTANT: This does NOT overwrite quantum_model.pth or touch any
file your live app depends on.
"""

import os
import copy
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader
import matplotlib.pyplot as plt

from quantum_model import HybridQuantumClassifier

RESULTS_FOLDER = "results"
os.makedirs(RESULTS_FOLDER, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using Device:", device)

X_train = np.load("X_train_quantum.npy")
X_test = np.load("X_test_quantum.npy")
y_train = np.load("y_train_quantum.npy")
y_test = np.load("y_test_quantum.npy")

X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.long)
y_test = torch.tensor(y_test, dtype=torch.long)

train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=64, shuffle=True)
test_loader = DataLoader(TensorDataset(X_test, y_test), batch_size=64, shuffle=False)

model = HybridQuantumClassifier().to(device)

criterion = torch.nn.CrossEntropyLoss(label_smoothing=0.1)
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-4, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="max", factor=0.5, patience=5)

epochs = 100
best_acc = 0
early_stop = 15
counter = 0

train_acc_history = []
val_acc_history = []

print("\nTraining a throwaway quantum model to capture history...\n")

for epoch in range(epochs):
    model.train()
    train_correct = 0
    train_total = 0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        pred = outputs.argmax(1)
        train_correct += (pred == labels).sum().item()
        train_total += labels.size(0)

    train_acc = 100 * train_correct / train_total

    model.eval()
    val_correct = 0
    val_total = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            pred = outputs.argmax(1)
            val_correct += (pred == labels).sum().item()
            val_total += labels.size(0)

    val_acc = 100 * val_correct / val_total

    scheduler.step(val_acc)

    train_acc_history.append(train_acc)
    val_acc_history.append(val_acc)

    print(f"Epoch {epoch+1:03d} | Train {train_acc:.2f}% | Val {val_acc:.2f}%")

    if val_acc > best_acc:
        best_acc = val_acc
        counter = 0
    else:
        counter += 1

    if counter >= early_stop:
        print("\nEarly Stopping...")
        break

np.save(os.path.join(RESULTS_FOLDER, "quantum_train_acc.npy"), np.array(train_acc_history))
np.save(os.path.join(RESULTS_FOLDER, "quantum_val_acc.npy"), np.array(val_acc_history))

mobilenet_val_path = os.path.join(RESULTS_FOLDER, "mobilenet_val_acc.npy")

if os.path.exists(mobilenet_val_path):
    mobilenet_val_acc = np.load(mobilenet_val_path) * 100
    mobilenet_epochs = range(1, len(mobilenet_val_acc) + 1)
else:
    print("\nWARNING: mobilenet_val_acc.npy not found. Run plot_training_curves.py first.")
    mobilenet_val_acc = None

quantum_epochs = range(1, len(val_acc_history) + 1)

plt.figure(figsize=(9, 6))

plt.plot(quantum_epochs, val_acc_history, label="Hybrid Quantum Model (Val Accuracy)", linewidth=2)

if mobilenet_val_acc is not None:
    plt.plot(mobilenet_epochs, mobilenet_val_acc, label="MobileNetV2 Classical (Val Accuracy)", linewidth=2)

plt.xlabel("Epoch")
plt.ylabel("Validation Accuracy (%)")
plt.title("Quantum vs Classical Model: Validation Accuracy Comparison")
plt.legend()
plt.grid(alpha=0.3)

save_path = os.path.join(RESULTS_FOLDER, "quantum_vs_classical_curves.png")
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"\nSaved: {save_path}")
print("Note: quantum_model.pth was NOT touched by this script.")
