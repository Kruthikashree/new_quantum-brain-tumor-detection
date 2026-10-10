import base64
import numpy as np
import cv2
import torch

from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from predict import feature_extractor, scaler, model, device, CLASS_NAMES, IMG_SIZE

PATCH_SIZE = 74
STRIDE = 74
OCCLUSION_COLOR = 0


def generate_explanation(image_path):

    img = keras_image.load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = keras_image.img_to_array(img).astype("uint8")

    # --- Baseline prediction ---
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
        all_probs = probabilities[0].cpu().numpy().tolist()

    # --- Build ALL occluded versions up front ---
    positions = list(range(0, IMG_SIZE - PATCH_SIZE + 1, STRIDE))
    coords = [(y, x) for y in positions for x in positions]

    batch = np.zeros((len(coords), IMG_SIZE, IMG_SIZE, 3), dtype="uint8")
    for i, (y, x) in enumerate(coords):
        occ = img_array.copy()
        occ[y:y+PATCH_SIZE, x:x+PATCH_SIZE, :] = OCCLUSION_COLOR
        batch[i] = occ

    # --- ONE batched call through MobileNet instead of N separate calls ---
    batch_arr = preprocess_input(batch.astype("float32"))
    batch_features = feature_extractor.predict(batch_arr, verbose=0, batch_size=len(coords))
    batch_features = scaler.transform(batch_features)
    batch_features_t = torch.tensor(batch_features, dtype=torch.float32).to(device)

    with torch.no_grad():
        batch_output = model(batch_features_t)
        batch_probs = torch.softmax(batch_output, dim=1)
        occluded_confs = batch_probs[:, predicted_class].cpu().numpy()

    # --- Build heatmap from the batched results ---
    heatmap = np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.float32)
    count_map = np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.float32)

    for (y, x), occluded_conf in zip(coords, occluded_confs):
        drop = baseline_conf - float(occluded_conf)
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
    probability_breakdown = {
        CLASS_NAMES[i]: round(p * 100, 2) for i, p in enumerate(all_probs)
    }

    return {
        "tumor": tumor,
        "confidence": confidence,
        "heatmap": heatmap_data_uri,
        "probabilities": probability_breakdown
    }