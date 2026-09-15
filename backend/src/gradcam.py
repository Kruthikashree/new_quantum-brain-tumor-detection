"""
gradcam.py

Grad-CAM Visualization for MobileNetV2
Quantum Enhanced Deep Learning for Brain Tumor Detection
"""

import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# --------------------------------------------------------
# Configuration
# --------------------------------------------------------

MODEL_PATH = "brain_tumor_mobilenet.keras"

IMG_SIZE = 224

CLASS_NAMES = [
    "Glioma",
    "Meningioma",
    "No Tumor",
    "Pituitary"
]

SAVE_FOLDER = "results"

os.makedirs(SAVE_FOLDER, exist_ok=True)

# --------------------------------------------------------
# Load Model
# --------------------------------------------------------

print("="*60)
print("Loading MobileNetV2 Model...")
print("="*60)

model = load_model(MODEL_PATH)

print("Model Loaded Successfully!\n")

# --------------------------------------------------------
# Build a Grad-CAM model directly on the base_model's own
# input/output graph, then re-apply the classifier head.
#
# NOTE: Reaching into an internal layer of a model that is
# itself nested as a layer inside another functional model
# (as MobileNetV2 is here) causes a "disconnected graph"
# error in recent TF/Keras versions. Rebuilding the head on
# base_model's own (already well-defined) input/output avoids
# that entirely, since include_top=False means base_model's
# own output IS already the last conv feature map.
# --------------------------------------------------------

base_model = model.layers[1]

gap_layer = model.layers[2]
dense1_layer = model.layers[3]
dropout_layer = model.layers[4]
dense2_layer = model.layers[5]

last_conv_output = base_model.output

x = gap_layer(last_conv_output)
x = dense1_layer(x)
x = dropout_layer(x, training=False)
predictions_tensor = dense2_layer(x)

grad_model = Model(
    inputs=base_model.input,
    outputs=[last_conv_output, predictions_tensor]
)

# --------------------------------------------------------
# Read Image
# --------------------------------------------------------

img_path = input("Enter MRI Image Path : ").strip()

img = image.load_img(
    img_path,
    target_size=(IMG_SIZE, IMG_SIZE)
)

img_array = image.img_to_array(img)

original_img = img_array.astype(np.uint8)

img_array = np.expand_dims(img_array, axis=0)

img_array = preprocess_input(img_array)

# --------------------------------------------------------
# Compute GradCAM
# --------------------------------------------------------

with tf.GradientTape() as tape:

    conv_outputs, predictions = grad_model(img_array)

    predicted_class = tf.argmax(predictions[0])

    loss = predictions[:, predicted_class]

grads = tape.gradient(loss, conv_outputs)

pooled_grads = tf.reduce_mean(grads, axis=(0,1,2))

conv_outputs = conv_outputs[0]

heatmap = tf.reduce_sum(
    pooled_grads * conv_outputs,
    axis=-1
)

heatmap = tf.maximum(heatmap,0)

heatmap = heatmap / (tf.reduce_max(heatmap)+1e-8)

heatmap = heatmap.numpy()

# --------------------------------------------------------
# Resize Heatmap
# --------------------------------------------------------

heatmap = cv2.resize(
    heatmap,
    (IMG_SIZE, IMG_SIZE)
)

heatmap_uint8 = np.uint8(255 * heatmap)

heatmap_color = cv2.applyColorMap(
    heatmap_uint8,
    cv2.COLORMAP_JET
)

overlay = cv2.addWeighted(
    original_img,
    0.6,
    heatmap_color,
    0.4,
    0
)

# --------------------------------------------------------
# Prediction
# --------------------------------------------------------

prediction = predictions.numpy()[0]

confidence = np.max(prediction) * 100

tumor = CLASS_NAMES[np.argmax(prediction)]

# --------------------------------------------------------
# Plot
# --------------------------------------------------------

plt.figure(figsize=(15,5))

plt.subplot(1,3,1)

plt.imshow(original_img.astype("uint8"))

plt.axis("off")

plt.title("Original MRI")

plt.subplot(1,3,2)

plt.imshow(heatmap, cmap="jet")

plt.axis("off")

plt.title("Grad-CAM Heatmap")

plt.subplot(1,3,3)

plt.imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))

plt.axis("off")

plt.title("Overlay")

plt.suptitle(
    f"Prediction : {tumor}    Confidence : {confidence:.2f}%",
    fontsize=14,
    fontweight="bold"
)

plt.tight_layout()

save_path = os.path.join(
    SAVE_FOLDER,
    "gradcam_result.png"
)

plt.savefig(
    save_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# --------------------------------------------------------
# Print Result
# --------------------------------------------------------

print("\n"+"="*60)

print("Prediction Result")

print("="*60)

print(f"Tumor Type : {tumor}")

print(f"Confidence : {confidence:.2f}%")

print(f"\nGradCAM Image Saved At : {save_path}")

print("="*60)
