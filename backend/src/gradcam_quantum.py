"""
gradcam_quantum.py

Explainability for the Hybrid Quantum Neural Network, using
Occlusion Sensitivity.

True gradient-based Grad-CAM cannot be applied directly to the
quantum branch of this pipeline: MobileNetV2 features are
globally average-pooled into a flat 1280-dim vector before
reaching the quantum classifier, which destroys the spatial
structure Grad-CAM needs, and the quantum circuit (PennyLane,
in a separate PyTorch graph) cannot be backpropagated through
the same computation graph as the TensorFlow feature extractor.

Occlusion Sensitivity instead measures, patch by patch, how much
the ACTUAL quantum model's confidence drops when that region of
the image is hidden. A larger drop means that region mattered more
to the prediction. This runs the real end-to-end pipeline (the
same one predict.py uses) for every patch, so it reflects the
quantum model's true behaviour rather than an approximation.
"""

import os
import numpy as np
import cv2
import torch
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from predict import feature_extractor, scaler, model, device, CLASS_NAMES, IMG_SIZE

SAVE_FOLDER = "results"
os.makedirs(SAVE_FOLDER, exist_ok=True)

PATCH_SIZE = 32
STRIDE = 32
OCCLUSION_COLOR = 0


def predict_confidence(img_array_uint8, target_class_index):
    arr = img_array_uint8.astype("float32")
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)

    features = feature_extractor.predict(arr, verbose=0)
    features = scaler.transform(features)
    features_t = torch.tensor(features, dtype=torch.float32).to(device)

    with torch.no_grad():
        output = model(features_t)
        probabilities = torch.softmax(output, dim=1)

    return probabilities[0, target_class_index].item()


def generate_occlusion_heatmap(image_path):

    img = keras_image.load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = keras_image.img_to_array(img).astype("uint8")

    arr = img_array.astype("float32")
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)

    features = feature_extractor.predict(arr, verbose=0)
    features = scaler.transform(features)
    features_t = torch.tensor(features, dtype=torch.float32).to(device)

    with torch.no_grad():
        output = model(features_t)
        probabilities = torch.softmax(output, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        baseline_conf = probabilities[0, predicted_class].item()

    print(f"Baseline Prediction: {CLASS_NAMES[predicted_class]} "
          f"({baseline_conf*100:.2f}% confidence)")

    heatmap = np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.float32)
    count_map = np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.float32)

    positions = list(range(0, IMG_SIZE - PATCH_SIZE + 1, STRIDE))
    total = len(positions) * len(positions)
    step = 0

    for y in positions:
        for x in positions:
            step += 1
            print(f"  Occluding patch {step}/{total}", end="\r")

            occluded = img_array.copy()
            occluded[y:y+PATCH_SIZE, x:x+PATCH_SIZE, :] = OCCLUSION_COLOR

            occluded_conf = predict_confidence(occluded, predicted_class)

            drop = baseline_conf - occluded_conf

            heatmap[y:y+PATCH_SIZE, x:x+PATCH_SIZE] += drop
            count_map[y:y+PATCH_SIZE, x:x+PATCH_SIZE] += 1

    print()

    count_map[count_map == 0] = 1
    heatmap = heatmap / count_map

    heatmap = np.maximum(heatmap, 0)
    if heatmap.max() > 0:
        heatmap = heatmap / heatmap.max()

    return img_array, heatmap, CLASS_NAMES[predicted_class], baseline_conf


if __name__ == "__main__":

    img_path = input("Enter MRI Image Path : ").strip().strip('"')

    original_img, heatmap, tumor, confidence = generate_occlusion_heatmap(img_path)

    heatmap_uint8 = np.uint8(255 * heatmap)
    heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)

    overlay = cv2.addWeighted(original_img, 0.6, heatmap_color, 0.4, 0)

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(original_img)
    plt.axis("off")
    plt.title("Original MRI")

    plt.subplot(1, 3, 2)
    plt.imshow(heatmap, cmap="jet")
    plt.axis("off")
    plt.title("Quantum Model Saliency Map")

    plt.subplot(1, 3, 3)
    plt.imshow(overlay)
    plt.axis("off")
    plt.title("Overlay")

    plt.suptitle(
        f"Prediction : {tumor}    Confidence : {confidence*100:.2f}%",
        fontsize=14,
        fontweight="bold"
    )

    plt.tight_layout()

    save_path = os.path.join(SAVE_FOLDER, "quantum_gradcam_result.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()

    print("\n" + "="*60)
    print("Prediction Result")
    print("="*60)
    print(f"Tumor Type : {tumor}")
    print(f"Confidence : {confidence*100:.2f}%")
    print(f"\nSaliency Map Saved At : {save_path}")
    print("="*60)
