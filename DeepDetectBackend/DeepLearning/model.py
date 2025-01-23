import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

# Dataset Paths
dataset_directory = "C:/Users/ss445/OneDrive/Desktop/Major/DeepDetectBackend/Dataset/"

# Custom contrast adjustment function
def adjust_contrast(image):
    image = image * 255.0  # Convert from range [0,1] to [0,255]
    image = np.uint8(image)  # Convert to integer values
    image = cv2.convertScaleAbs(image, alpha=1.5, beta=0)  # Increase contrast
    return image / 255.0  # Normalize back to [0,1]

# ImageDataGenerator with enhanced augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.3,
    brightness_range=[0.8, 1.2],
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2,
    preprocessing_function=adjust_contrast
)

valid_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

# Data Generators
train_generator = train_datagen.flow_from_directory(
    dataset_directory,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

valid_generator = valid_datagen.flow_from_directory(
    dataset_directory,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

# Class Weights to handle imbalance
from sklearn.utils.class_weight import compute_class_weight

labels = train_generator.classes  # Get class labels
class_weights = compute_class_weight('balanced', classes=np.unique(labels), y=labels)
class_weight_dict = {i: class_weights[i] for i in range(len(class_weights))}

# Load EfficientNetB0 (Fine-Tuning)
base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Unfreeze half of the model layers
for layer in base_model.layers[:len(base_model.layers) // 2]:
    layer.trainable = False
for layer in base_model.layers[len(base_model.layers) // 2:]:
    layer.trainable = True

# Build Model
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    BatchNormalization(),
    Dense(512, activation='relu'),
    Dropout(0.3),
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])

# Compile Model with SGD optimizer
model.compile(
    optimizer=SGD(learning_rate=0.01, momentum=0.9, nesterov=True),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Callbacks
callbacks = [
    EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-7, verbose=1),
    ModelCheckpoint(filepath='best_efficientnet_model_v3.keras', save_best_only=True, monitor='val_loss', verbose=1)
]

# Train Model with Class Weights
history = model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    validation_data=valid_generator,
    validation_steps=len(valid_generator),
    epochs=30,
    callbacks=callbacks,
    class_weight=class_weight_dict  # Apply class weights
)

# Save Model
model.save('efficientnet_deepfake_detector_v3.keras')
