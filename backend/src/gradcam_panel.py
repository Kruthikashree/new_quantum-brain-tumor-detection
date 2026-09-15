"""
gradcam_panel.py

Generates a 4-row Grad-CAM panel (Original | Heatmap | Overlay),
one representative example per tumor class, for the report figure
"gradcam_panel_all_classes.png".
"""

import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

MODEL_PATH = "brain_tumor_mobilenet.keras"
IMG_SIZE = 224
SAVE_FOLDER = "results"
os.makedirs(SAVE_FOLDER, exist_ok=True)

CLASSES = {
    "Glioma": "dataset/brain_tumor/Testing/glioma",
    "Meningioma": "dataset/brain_tumor/Testing/meningioma",
    "No Tumor": "dataset/brain_tumor/Testing/notumor",
    "Pituitary": "dataset/brain_tumor/Testing/pituitary",
}

CLASS_NAMES = ["Glioma", "Meningioma", "No Tumor", "Pituitary"]

print("Loading model...")
model = load_model(MODEL_PATH)

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


def compute_gradcam(img_path):
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    original_img = img_array.astype(np.uint8)

    arr = np.expand_dims(img_array, axis=0)
    arr = preprocess_input(arr)

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(arr)
        predicted_class = tf.argmax(predictions[0])
        loss = predictions[:, predicted_class]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]

    heatmap = tf.reduce_sum(pooled_grads * conv_outputs, axis=-1)
    heatmap = tf.maximum(heatmap, 0)
    heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8)
    heatmap = heatmap.numpy()

    heatmap_resized = cv2.resize(heatmap, (IMG_SIZE, IMG_SIZE))
    heatmap_uint8 = np.uint8(255 * heatmap_resized)
    heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(original_img, 0.6, heatmap_color, 0.4, 0)

    return original_img, heatmap_resized, cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)


fig, axes = plt.subplots(4, 3, figsize=(8, 10.5))

plt.subplots_adjust(wspace=0.03, hspace=0.12, left=0.14, right=0.98, top=0.94, bottom=0.02)

for row, class_name in enumerate(CLASS_NAMES):
    folder = CLASSES[class_name]
    filename = sorted(os.listdir(folder))[0]
    img_path = os.path.join(folder, filename)

    original_img, heatmap, overlay = compute_gradcam(img_path)

    axes[row, 0].imshow(original_img)
    axes[row, 0].set_xticks([])
    axes[row, 0].set_yticks([])

    axes[row, 1].imshow(heatmap, cmap="jet")
    axes[row, 1].set_xticks([])
    axes[row, 1].set_yticks([])

    axes[row, 2].imshow(overlay)
    axes[row, 2].set_xticks([])
    axes[row, 2].set_yticks([])

    axes[row, 0].set_ylabel(
        class_name,
        fontsize=13,
        fontweight="bold",
        rotation=0,
        labelpad=55,
        va="center"
    )

axes[0, 0].set_title("Original MRI", fontsize=13)
axes[0, 1].set_title("Grad-CAM Heatmap", fontsize=13)
axes[0, 2].set_title("Overlay", fontsize=13)

save_path = os.path.join(SAVE_FOLDER, "gradcam_panel_all_classes.png")
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"\nSaved: {save_path}")
