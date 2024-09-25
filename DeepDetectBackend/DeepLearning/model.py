# deeplearning/model.py

import os
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

AUTOTUNE = tf.data.AUTOTUNE

# Function to load images and preprocess
def load_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [224, 224])
    image = image / 255.0
    return image

# Function to parse data from CSV
def parse_data(row, root_dir):
    image_path = os.path.join(root_dir, row['path'])
    label = tf.convert_to_tensor(row['label'], dtype=tf.int32)
    image = load_image(image_path)
    return image, label

# Function to load dataset
def load_dataset(csv_file, root_dir, batch_size=32, shuffle=True):
    df = pd.read_csv(csv_file)
    dataset = tf.data.Dataset.from_tensor_slices(dict(df))
    dataset = dataset.map(lambda row: parse_data(row, root_dir), num_parallel_calls=AUTOTUNE)
    
    if shuffle:
        dataset = dataset.shuffle(buffer_size=len(df))
    
    dataset = dataset.batch(batch_size).prefetch(buffer_size=AUTOTUNE)
    
    return dataset

# Load the train and validation datasets
train_dataset = load_dataset('../Dataset/train.csv', '../Dataset/rvf10k/train')
valid_dataset = load_dataset('../Dataset/valid.csv', '../Dataset/rvf10k/valid')


# Function to create the deepfake detection model
def create_model(input_shape=(224, 224, 3)):
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=input_shape)
    base_model.trainable = False  # Freeze the base model

    # Custom layers on top of MobileNetV2
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')  # Binary classification (real/fake)
    ])

    # Compile the model
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    return model

# Create the model
model = create_model()

# Display model architecture
model.summary()

# Train the model
history = model.fit(
    train_dataset,
    epochs=10,
    validation_data=valid_dataset
)

# Save the trained model
model.save('deeplearning/deepfake_model.h5')
