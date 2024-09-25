from fastapi import FastAPI, File, UploadFile
import uvicorn  # Import uvicorn programmatically

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to DeepDetect API"}

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    return {"filename": file.filename}

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    return {"filename": file.filename}

# Add this to allow the script to run with "python main.py"
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
