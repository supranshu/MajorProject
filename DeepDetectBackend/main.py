from fastapi import FastAPI, File, UploadFile
from fastapi.exceptions import HTTPException
import uvicorn
from tensorflow.keras.models import load_model
import numpy as np
import cv2
from PIL import Image
import io
import os
from pydantic import BaseModel
import requests  
from dotenv import load_dotenv

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the pre-trained model once when the application starts
MODEL_PATH = "./TrainedModel/best_model_new.keras"
model = load_model(MODEL_PATH)


load_dotenv() 

GEMINI_URL = os.getenv("GEMINI_API_URL")
GEMINI_KEY = os.getenv("GEMINI_API_KEY") 

class QueryRequest(BaseModel):
    question: str

@app.post("/ask-deepfake/")
async def ask_deepfake(request: QueryRequest):
    question = request.question

    prompt = f"Answer only questions related to deepfake images and videos and answer in 2-3 sentences only. If the query is unrelated, respond with: 'Sorry, this topic is out of our discussion .'\nUser Query: {question}"

    request_data = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(f"{GEMINI_URL}?key={GEMINI_KEY}", json=request_data)

    if response.status_code == 200:
        data = response.json()
        reply = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Error fetching response")
        return {"response": reply}
    else:
        return {"error": "Failed to communicate with Gemini API", "status_code": response.status_code}




# Helper function: Preprocess image
def preprocess_image(image_bytes):
    try:
        # Attempt to open the image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        raise ValueError(f"Failed to process image. Error: {e}")

    # Resize and preprocess
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array


# Helper function: Process video and predict for each frame
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        # Convert frame to RGB and preprocess
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame_rgb)
        frame_image = frame_image.resize((224, 224))
        frame_array = np.array(frame_image) / 255.0
        frame_array = np.expand_dims(frame_array, axis=0)

        # Predict using the model
        prediction = model.predict(frame_array)

        # If ANY value in prediction is greater than 0.2, return deepfake
        if np.any(prediction > 0.5):
            cap.release()
            return {"is_fake": True, "confidence": float(np.max(prediction)), "total_frames": frame_count}

    cap.release()
    return {"is_fake": False, "confidence": 0.0, "total_frames": frame_count}


@app.get("/")
def read_root():
    return {"message": "Welcome to DeepDetect API"}


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # Read image bytes
    image_bytes = await file.read()

    # Preprocess the image
    processed_image = preprocess_image(image_bytes)

    # Predict using the model
    prediction = model.predict(processed_image)
    is_fake = prediction[0][0] > 0.1 

    print(f"Prediction output: {prediction}")


    return {
        "filename": file.filename,
        "is_fake": bool(is_fake),  # Convert numpy.bool to native bool
        "confidence": float(prediction[0][0]),  # Convert to float for JSON serialization
    }


@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    video_path = f"temp_{file.filename}"
    with open(video_path, "wb") as video_file:
        video_file.write(await file.read())

    result = process_video(video_path)
    
    os.remove(video_path)  # Clean up the file

    return {"filename": file.filename, **result}


# Add this to allow the script to run with "python main.py"
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
