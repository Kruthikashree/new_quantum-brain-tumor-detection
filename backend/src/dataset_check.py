import os
import matplotlib.pyplot as plt
from PIL import Image


train_path = "dataset/brain_tumor/Training"

classes = os.listdir(train_path)

print("Classes found:")
print(classes)


print("\nTraining image count:")

for cls in classes:
    folder = os.path.join(train_path, cls)
    count = len(os.listdir(folder))
    print(cls, ":", count)


plt.figure(figsize=(12,4))

for i, cls in enumerate(classes):

    folder = os.path.join(train_path, cls)

    image_name = os.listdir(folder)[0]

    image_path = os.path.join(folder, image_name)

    img = Image.open(image_path)

    plt.subplot(1,4,i+1)
    plt.imshow(img)
    plt.title(cls)
    plt.axis("off")


plt.show()