import os
import numpy as np
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

# Dataset Paths
dataset_directory = "C:/Users/ss445/OneDrive/Desktop/Major/DeepDetectBackend/Dataset/"

# Enhanced Data Augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,  
    width_shift_range=0.3,
    height_shift_range=0.3,
    shear_range=0.3,
    zoom_range=0.3,
    brightness_range=[0.6, 1.4],  # Stronger brightness variations
    channel_shift_range=0.3,  # Simulates lighting conditions
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2  
)

# Train and Validation Generators
train_generator = train_datagen.flow_from_directory(
    dataset_directory,
    target_size=(224, 224),
    batch_size=64,  # Increase batch size to generalize better
    class_mode='binary',
    subset='training'
)

valid_generator = train_datagen.flow_from_directory(
    dataset_directory,
    target_size=(224, 224),
    batch_size=64,
    class_mode='binary',
    subset='validation'
)

# Load Pretrained VGG16
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze More Layers Initially
for layer in base_model.layers[:-6]:  # Freeze all but the last 6 layers
    layer.trainable = False

# Build Model
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    BatchNormalization(),
    Dense(128, activation='relu', kernel_regularizer='l2'),  # Reduce neurons, L2 regularization
    Dropout(0.6),  # Increased dropout
    Dense(1, activation='sigmoid')
])

# Compile Model with Lower Learning Rate
model.compile(
    optimizer=Adam(learning_rate=1e-5),  # Reduce learning rate
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Callbacks
callbacks = [
    EarlyStopping(monitor='val_loss', patience=7, restore_best_weights=True, verbose=1),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-7, verbose=1),
    ModelCheckpoint(filepath='best_model_new1.keras', save_best_only=True, monitor='val_loss', verbose=1)
]

# Train Model
history = model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    validation_data=valid_generator,
    validation_steps=len(valid_generator),
    epochs=30,  # Train longer with lower learning rate
    callbacks=callbacks
)

# Save Model
model.save('vgg16_deepfake_detector_new1.keras')
