"""
plot_training_curves.py

Re-trains a FRESH, THROWAWAY copy of the MobileNetV2 classifier
(same architecture/hyperparameters as train_mobilenet.py) purely to
capture epoch-by-epoch accuracy/loss history for plotting.

IMPORTANT: This does NOT overwrite brain_tumor_mobilenet.keras or
touch any file your live app depends on. History arrays are saved
to .npy files so plot_quantum_vs_classical.py can reuse them
without retraining again.
"""

import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from mobilenet_model import model

train_dir = "dataset/brain_tumor/Training"
test_dir = "dataset/brain_tumor/Testing"

RESULTS_FOLDER = "results"
os.makedirs(RESULTS_FOLDER, exist_ok=True)

train_ds = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=(224, 224),
    batch_size=32
)

test_ds = tf.keras.utils.image_dataset_from_directory(
    test_dir,
    image_size=(224, 224),
    batch_size=32
)

print("Training a throwaway copy to capture history (won't overwrite your saved model)...")

history = model.fit(
    train_ds,
    validation_data=test_ds,
    epochs=10
)

np.save(os.path.join(RESULTS_FOLDER, "mobilenet_train_acc.npy"), history.history["accuracy"])
np.save(os.path.join(RESULTS_FOLDER, "mobilenet_val_acc.npy"), history.history["val_accuracy"])
np.save(os.path.join(RESULTS_FOLDER, "mobilenet_train_loss.npy"), history.history["loss"])
np.save(os.path.join(RESULTS_FOLDER, "mobilenet_val_loss.npy"), history.history["val_loss"])

epochs_range = range(1, len(history.history["accuracy"]) + 1)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(epochs_range, history.history["accuracy"], label="Train Accuracy")
plt.plot(epochs_range, history.history["val_accuracy"], label="Val Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("MobileNetV2 Accuracy")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(epochs_range, history.history["loss"], label="Train Loss")
plt.plot(epochs_range, history.history["val_loss"], label="Val Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("MobileNetV2 Loss")
plt.legend()

plt.tight_layout()

save_path = os.path.join(RESULTS_FOLDER, "training_curves.png")
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"\nSaved: {save_path}")
print("Note: brain_tumor_mobilenet.keras was NOT touched by this script.")
