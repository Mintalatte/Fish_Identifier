import pandas as pd
import os
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Define imsage Data scale and batch size
shrinking = 4
img_height = int(1944 / shrinking)
img_width = int(2592 / shrinking)
input_shape = (img_height, img_width, 3)
batch_size = 16

# defining dataset directory
dataset_dir = "dataset"

# Get a list of all image file paths
file_paths = []
labels = []

for class_label, class_name in enumerate(os.listdir(dataset_dir)):
    class_dir = os.path.join(dataset_dir, class_name)
    for image_name in os.listdir(class_dir):
        file_paths.append(os.path.join(class_dir, image_name))
        labels.append(class_label)
        # print(image_name, class_label)

# DataFrame with file paths and labels        
data = pd.DataFrame({
    'file_path': file_paths,
    'label': labels
})

# Split the dataset into train and test sets
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# generate datagenerator
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_dataframe(
    train_data,
    x_col='file_path',
    y_col='label',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='raw'  # Use 'raw' for integer labels
)

test_generator = test_datagen.flow_from_dataframe(
    test_data,
    x_col='file_path',
    y_col='label',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='raw'
)

model = tf.keras.Sequential([
    Conv2D(32, (15, 15), activation='relu', input_shape=input_shape),
    MaxPooling2D((2, 2)),
    Conv2D(64, (15, 15), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(2, activation='softmax')  # Output layer with appropriate number of units
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples,
    epochs=10,
    validation_data=test_generator,
    validation_steps=test_generator.samples,
)

test_loss, test_acc = model.evaluate(test_generator, verbose=2)
print('\nTest accuracy:', test_acc)