"""
train_quantum.py

Train Improved Hybrid Quantum Neural Network
"""

import copy
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader

from quantum_model import HybridQuantumClassifier

# ---------------------------------------------------
# Device
# ---------------------------------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Using Device:", device)

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

print("\nLoading Features...")

X_train = np.load("X_train_quantum.npy")
X_test = np.load("X_test_quantum.npy")

y_train = np.load("y_train_quantum.npy")
y_test = np.load("y_test_quantum.npy")

print("Train:", X_train.shape)
print("Test :", X_test.shape)

# ---------------------------------------------------
# Torch Tensor
# ---------------------------------------------------

X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)

y_train = torch.tensor(y_train, dtype=torch.long)
y_test = torch.tensor(y_test, dtype=torch.long)

# ---------------------------------------------------
# DataLoader
# ---------------------------------------------------

train_loader = DataLoader(
    TensorDataset(X_train, y_train),
    batch_size=64,
    shuffle=True
)

test_loader = DataLoader(
    TensorDataset(X_test, y_test),
    batch_size=64,
    shuffle=False
)

# ---------------------------------------------------
# Model
# ---------------------------------------------------

model = HybridQuantumClassifier().to(device)

criterion = torch.nn.CrossEntropyLoss(label_smoothing=0.1)

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=5e-4,
    weight_decay=1e-4
)

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="max",
    factor=0.5,
    patience=5
)

epochs = 100

best_acc = 0
best_weights = copy.deepcopy(model.state_dict())

early_stop = 15
counter = 0

print("\nTraining Started...\n")

# ---------------------------------------------------
# Training Loop
# ---------------------------------------------------

for epoch in range(epochs):

    model.train()

    train_correct = 0
    train_total = 0
    train_loss = 0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            model.parameters(),
            1.0
        )

        optimizer.step()

        train_loss += loss.item()

        pred = outputs.argmax(1)

        train_correct += (pred == labels).sum().item()

        train_total += labels.size(0)

    train_acc = 100 * train_correct / train_total

    # ---------------- Validation ----------------

    model.eval()

    val_correct = 0
    val_total = 0

    with torch.no_grad():

        for images, labels in test_loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            pred = outputs.argmax(1)

            val_correct += (pred == labels).sum().item()

            val_total += labels.size(0)

    val_acc = 100 * val_correct / val_total

    scheduler.step(val_acc)

    print(
        f"Epoch {epoch+1:03d} | "
        f"Loss {train_loss:.2f} | "
        f"Train {train_acc:.2f}% | "
        f"Val {val_acc:.2f}%"
    )

    if val_acc > best_acc:

        best_acc = val_acc
        best_weights = copy.deepcopy(model.state_dict())
        counter = 0

    else:

        counter += 1

    if counter >= early_stop:

        print("\nEarly Stopping...")
        break

# ---------------------------------------------------
# Save Best Model
# ---------------------------------------------------

model.load_state_dict(best_weights)

torch.save(
    model.state_dict(),
    "quantum_model.pth"
)

print("\n================================")
print("Training Completed")
print("================================")
print(f"Best Validation Accuracy: {best_acc:.2f}%")
print("Model Saved Successfully!")