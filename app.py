from fastapi import FastAPI, UploadFile, File
import torch
from PIL import Image
import io
from ultralytics import YOLO

app = FastAPI()
model = YOLO("best.pt")  # Load trained model

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    results = model(image)
    
    return {"detections": results.pandas().xyxy[0].to_dict(orient="records")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
