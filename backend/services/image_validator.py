import numpy as np
from PIL import Image

MIN_SIZE = 50
COLOR_PIXEL_THRESHOLD = 22      # a pixel is "colorful" if its channel spread exceeds this
COLOR_FRACTION_LIMIT = 0.03     # reject if more than 3% of pixels are colorful
MIN_STD = 8                     # rejects blank / solid-colour images


def looks_like_mri(pil_img):
    """
    Lightweight heuristic filter that catches obviously-wrong uploads
    (colour photos, screenshots, UI captures, solid-colour images) before
    they reach the model. This is NOT a medical validity check — it only
    rejects images that clearly cannot be a grayscale brain MRI scan.
    Returns (ok: bool, message: str).
    """
    try:
        img = pil_img.convert("RGB")
    except Exception:
        return False, "Could not read the uploaded image."

    w, h = img.size
    if w < MIN_SIZE or h < MIN_SIZE:
        return False, "The image is too small to be a valid MRI scan."

    img = img.resize((160, 160))
    arr = np.asarray(img).astype("float32")
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]

    # Per-pixel channel spread: near 0 for grayscale, high for real colour.
    spread = (np.abs(r - g) + np.abs(g - b) + np.abs(r - b)) / 3

    colorful_fraction = np.mean(spread > COLOR_PIXEL_THRESHOLD)
    if colorful_fraction > COLOR_FRACTION_LIMIT:
        return False, (
            "This does not look like a grayscale MRI scan. "
            "Please upload an actual brain MRI image."
        )

    gray = arr.mean(axis=2)
    if gray.std() < MIN_STD:
        return False, "The uploaded image appears blank or has too little detail to be an MRI scan."

    return True, ""