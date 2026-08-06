import tensorflow as tf
from mobilenet_model import model

train_dir = "dataset/brain_tumor/Training"
test_dir = "dataset/brain_tumor/Testing"

IMG_SIZE = 224
BATCH_SIZE = 32

# Load datasets
train_dataset = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=True
)

test_dataset = tf.keras.utils.image_dataset_from_directory(
    test_dir,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=False
)

# Normalize
normalization_layer = tf.keras.layers.Rescaling(1./255)

train_dataset = train_dataset.map(
    lambda x, y: (normalization_layer(x), y)
)

test_dataset = test_dataset.map(
    lambda x, y: (normalization_layer(x), y)
)

# Train
history = model.fit(
    train_dataset,
    validation_data=test_dataset,
    epochs=10
)

# Save model
model.save("brain_tumor_mobilenet.keras")

print("Training completed!")