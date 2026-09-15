import base64
import numpy as np
import cv2
import torch

from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from predict import feature_extractor, scaler, model, device, CLASS_NAMES, IMG_SIZE

PATCH_SIZE = 32
STRIDE = 32
OCCLUSION_COLOR = 0


def _predict_confidence(img_array_uint8, target_class_index):
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


def generate_explanation(image_path):

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

    heatmap = np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.float32)
    count_map = np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.float32)

    positions = list(range(0, IMG_SIZE - PATCH_SIZE + 1, STRIDE))

    for y in positions:
        for x in positions:
            occluded = img_array.copy()
            occluded[y:y+PATCH_SIZE, x:x+PATCH_SIZE, :] = OCCLUSION_COLOR

            occluded_conf = _predict_confidence(occluded, predicted_class)
            drop = baseline_conf - occluded_conf

            heatmap[y:y+PATCH_SIZE, x:x+PATCH_SIZE] += drop
            count_map[y:y+PATCH_SIZE, x:x+PATCH_SIZE] += 1

    count_map[count_map == 0] = 1
    heatmap = heatmap / count_map
    heatmap = np.maximum(heatmap, 0)

    if heatmap.max() > 0:
        heatmap = heatmap / heatmap.max()

    heatmap_uint8 = np.uint8(255 * heatmap)
    heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    heatmap_color_rgb = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)

    overlay = cv2.addWeighted(img_array, 0.6, heatmap_color_rgb, 0.4, 0)

    success, buffer = cv2.imencode(
        ".png",
        cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR)
    )

    heatmap_base64 = base64.b64encode(buffer).decode("utf-8")
    heatmap_data_uri = f"data:image/png;base64,{heatmap_base64}"

    tumor = CLASS_NAMES[predicted_class]
    confidence = round(baseline_conf * 100, 2)

    return {
        "tumor": tumor,
        "confidence": confidence,
        "heatmap": heatmap_data_uri
    }
