import os
import numpy as np
import tensorflow as tf

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image

# ----------------------------
# Paths
# ----------------------------

train_dir = "dataset/brain_tumor/Training"
test_dir = "dataset/brain_tumor/Testing"

IMG_SIZE = 224

# ----------------------------
# MobileNetV2 Feature Extractor
# ----------------------------

base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    pooling="avg",
    input_shape=(224, 224, 3)
)

# ----------------------------
# Function
# ----------------------------

def extract_features(dataset_path):

    features = []
    labels = []

    class_names = sorted(os.listdir(dataset_path))

    print("Classes:", class_names)

    for label, class_name in enumerate(class_names):

        class_path = os.path.join(dataset_path, class_name)

        for img_name in os.listdir(class_path):

            img_path = os.path.join(class_path, img_name)

            img = image.load_img(
                img_path,
                target_size=(IMG_SIZE, IMG_SIZE)
            )

            img_array = image.img_to_array(img)

            img_array = np.expand_dims(img_array, axis=0)

            img_array = preprocess_input(img_array)

            feature = base_model.predict(
                img_array,
                verbose=0
            )

            features.append(feature[0])

            labels.append(label)

    return np.array(features), np.array(labels)


# ----------------------------
# Extract
# ----------------------------

print("Extracting training features...")

X_train, y_train = extract_features(train_dir)

print("Extracting testing features...")

X_test, y_test = extract_features(test_dir)

# ----------------------------
# Save
# ----------------------------

np.save("X_train.npy", X_train)
np.save("y_train.npy", y_train)

np.save("X_test.npy", X_test)
np.save("y_test.npy", y_test)

print("\nFeature extraction completed!")

print("Training Features:", X_train.shape)
print("Testing Features :", X_test.shape)