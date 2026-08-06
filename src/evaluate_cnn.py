import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score
)

# ===========================
# Load Trained Model
# ===========================

model = tf.keras.models.load_model("brain_tumor_cnn.keras")

# ===========================
# Dataset Path
# ===========================

test_dir = "dataset/brain_tumor/Testing"

IMG_SIZE = 224
BATCH_SIZE = 32

# ===========================
# Load Test Dataset
# ===========================

test_dataset = tf.keras.utils.image_dataset_from_directory(
    test_dir,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=False
)

# Save class names BEFORE map()
class_names = test_dataset.class_names

normalization_layer = tf.keras.layers.Rescaling(1./255)

test_dataset = test_dataset.map(
    lambda x, y: (normalization_layer(x), y)
)

# ===========================
# Predict
# ===========================

y_true = []
y_pred = []

for images, labels in test_dataset:

    predictions = model.predict(images, verbose=0)

    predicted_labels = np.argmax(predictions, axis=1)

    y_true.extend(labels.numpy())
    y_pred.extend(predicted_labels)

# ===========================
# Accuracy
# ===========================

accuracy = accuracy_score(y_true, y_pred)

print("\n==============================")
print(f"Test Accuracy: {accuracy*100:.2f}%")
print("==============================")

# ===========================
# Classification Report
# ===========================

print("\nClassification Report\n")

print(classification_report(
    y_true,
    y_pred,
    target_names=class_names
))

# ===========================
# Confusion Matrix
# ===========================

cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(8,6))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=class_names,
    yticklabels=class_names
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.savefig("confusion_matrix.png")

plt.show()

print("\nConfusion matrix saved as confusion_matrix.png")