# DeepDetect: AI-Powered Deepfake Detection

## Overview
DeepDetect is a deepfake detection tool that uses a VGG16-based machine learning model to classify images and videos as real or AI-generated. The project consists of a FastAPI backend and an Angular frontend for an interactive user experience.

## Features
- **Image Detection**: Analyze images for deepfake manipulations.
- **Video Detection**: Process video frames to identify AI-generated content.
- **Real-Time Analysis**: Get instant results for media verification.

## Tech Stack
- **Backend**: FastAPI, TensorFlow/Keras, OpenCV, PIL
- **Frontend**: Angular
- **Model**: VGG16-based Convolutional Neural Network

## Installation
### Prerequisites
- Python 3.8+
- Node.js & Angular CLI (for frontend)
- pip & virtualenv

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/DeepDetect.git
   cd DeepDetect/DeepDetectBackend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend should now be running at `http://127.0.0.1:8000`.

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd ../DeepDetectFront
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the Angular development server:
   ```bash
   ng serve
   ```
   The frontend should be accessible at `http://localhost:4200`.

## Usage
- Open `http://localhost:4200` in your browser.
- Upload an image or video for deepfake detection.
- View results in real-time.

## API Endpoints
- `POST /upload-image/`: Upload an image for deepfake detection.
- `POST /upload-video/`: Upload a video for frame-by-frame analysis.

## Model Training
- The dataset is structured into `AI` and `real` directories.
- The model uses VGG16 as a feature extractor.
- Training includes data augmentation and regularization.

## Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes and push to your fork.
4. Open a Pull Request.


## Contact
For any questions or issues, feel free to reach out via GitHub Issues or email.

