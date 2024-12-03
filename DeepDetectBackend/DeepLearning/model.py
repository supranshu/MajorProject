import os
import pandas as pd
import numpy as np
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

# Dataset Paths
train_csv_path = "C:/Users/ss445/OneDrive/Desktop/Major/DeepDetectBackend/Dataset/train.csv"
valid_csv_path = "C:/Users/ss445/OneDrive/Desktop/Major/DeepDetectBackend/Dataset/valid.csv"
train_directory = "C:/Users/ss445/OneDrive/Desktop/Major/DeepDetectBackend/Dataset/rvf10k/"
valid_directory = "C:/Users/ss445/OneDrive/Desktop/Major/DeepDetectBackend/Dataset/rvf10k/"


# Load and Preprocess the CSV Files
train_df = pd.read_csv(train_csv_path)
valid_df = pd.read_csv(valid_csv_path)

train_df['label'] = train_df['label'].apply(lambda x: 'real' if x == 1 else 'fake')
valid_df['label'] = valid_df['label'].apply(lambda x: 'real' if x == 1 else 'fake')

train_df['path'] = train_df['path'].apply(lambda x: os.path.join(train_directory, x))
valid_df['path'] = valid_df['path'].apply(lambda x: os.path.join(valid_directory, x))

# Remove non-existent paths
train_df = train_df[train_df['path'].apply(os.path.exists)]
valid_df = valid_df[valid_df['path'].apply(os.path.exists)]

# Image Data Generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)
valid_datagen = ImageDataGenerator(rescale=1./255)

# Data Generators
train_generator = train_datagen.flow_from_dataframe(
    dataframe=train_df,
    x_col="path",
    y_col="label",
    target_size=(224, 224),  # Match the original VGG16 input size
    batch_size=32,
    class_mode='binary'
)
valid_generator = valid_datagen.flow_from_dataframe(
    dataframe=valid_df,
    x_col="path",
    y_col="label",
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

# VGG16 Model (Pretrained)
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Unfreeze the top layers for fine-tuning
for layer in base_model.layers[:-4]:  # Keep the first few layers frozen
    layer.trainable = False

# Build the Model
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),  # Better than Flatten for feature extraction
    BatchNormalization(),
    Dense(256, activation='relu'),
    Dropout(0.5),  # Prevents overfitting
    Dense(1, activation='sigmoid')  # Binary classification
])

# Compile the Model
model.compile(
    optimizer=Adam(learning_rate=1e-4),  # Initial learning rate
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Callbacks
callbacks = [
    EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1),
    ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6, verbose=1),
    ModelCheckpoint(filepath='best_model.h5', save_best_only=True, monitor='val_loss', verbose=1)
]

# Train the Model
history = model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    validation_data=valid_generator,
    validation_steps=len(valid_generator),
    epochs=20,  # Longer training with early stopping
    callbacks=callbacks
)

# Save the Final Model
model.save('vgg16_deepfake_detector_advanced.h5')
