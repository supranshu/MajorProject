import os
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam

# Set dataset paths
train_csv_path = './Dataset/train.csv'
valid_csv_path = './Dataset/valid.csv'
train_directory = './Dataset/rvf10k/'
valid_directory = './Dataset/rvf10k/'

# Load the CSV files
train_df = pd.read_csv(train_csv_path)
valid_df = pd.read_csv(valid_csv_path)

# Convert integer labels to strings for binary classification
train_df['label'] = train_df['label'].apply(lambda x: 'real' if x == 1 else 'fake')
valid_df['label'] = valid_df['label'].apply(lambda x: 'real' if x == 1 else 'fake')

# Update the path column to be the full path of the images
# Remove any extra 'train/' or 'valid/' prefix in the path
train_df['path'] = train_df['path'].apply(lambda x: os.path.join(train_directory, x))
valid_df['path'] = valid_df['path'].apply(lambda x: os.path.join(valid_directory, x))

# Print constructed paths for debugging
print("Train DataFrame Paths:")
print(train_df['path'].head())

print("Validation DataFrame Paths:")
print(valid_df['path'].head())

# Filter out any rows where the image path does not exist
train_df = train_df[train_df['path'].apply(os.path.exists)]
valid_df = valid_df[valid_df['path'].apply(os.path.exists)]

# Print the filtered DataFrame lengths
print(f"Filtered Training DataFrame Length: {len(train_df)}")
print(f"Filtered Validation DataFrame Length: {len(valid_df)}")

# Check for unique labels
print("Unique labels in training data:", train_df['label'].unique())
print("Unique labels in validation data:", valid_df['label'].unique())

# Image Data Generators for Data Augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

valid_datagen = ImageDataGenerator(rescale=1./255)

# Create Data Generators
train_generator = train_datagen.flow_from_dataframe(
    dataframe=train_df,
    directory=None,  # Set to None because paths are absolute
    x_col="path",
    y_col="label",
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

valid_generator = valid_datagen.flow_from_dataframe(
    dataframe=valid_df,
    directory=None,  # Set to None because paths are absolute
    x_col="path",
    y_col="label",
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

# Build the VGG16 model
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model = Sequential()
model.add(base_model)
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))  # Binary classification

# Compile the model
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    validation_data=valid_generator,
    validation_steps=len(valid_generator),
    epochs=10  # Adjust the number of epochs as needed
)

# Save the model
model.save('deepfake_detector_model.h5')
