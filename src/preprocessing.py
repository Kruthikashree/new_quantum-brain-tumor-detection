import tensorflow as tf
print("Script started")

# Dataset paths
train_dir = "dataset/brain_tumor/Training"
test_dir = "dataset/brain_tumor/Testing"


# Image parameters
IMG_SIZE = 224
BATCH_SIZE = 32


# Load training data
train_dataset = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=True
)


# Load testing data
test_dataset = tf.keras.utils.image_dataset_from_directory(
    test_dir,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=False
)


# Class names
print("Classes:")
print(train_dataset.class_names)


# Normalize images
normalization_layer = tf.keras.layers.Rescaling(1./255)


train_dataset = train_dataset.map(
    lambda x, y: (normalization_layer(x), y)
)


test_dataset = test_dataset.map(
    lambda x, y: (normalization_layer(x), y)
)


# Check one batch

for images, labels in train_dataset.take(1):
    print("Image shape:", images.shape)
    print("Label shape:", labels.shape)