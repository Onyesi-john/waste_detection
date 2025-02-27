import os
from ultralytics import YOLO

# Define paths dynamically to avoid hardcoding
BASE_DIR = os.path.expanduser("~/waste_detection")  # Change this if needed
MODEL_PATH = os.path.join(BASE_DIR, "models", "yolov5nu.pt")
DATA_PATH = os.path.join(BASE_DIR, "dataset", "data.yaml")
OUTPUT_DIR = os.path.join(BASE_DIR, "runs", "train", "exp", "weights")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Loading YOLO model from: {MODEL_PATH}")
model = YOLO(MODEL_PATH)

print(f"Starting training with data: {DATA_PATH}")
model.train(
    data=DATA_PATH,  
    epochs=50,
    batch=8,
    imgsz=416,
)

# Ensure best.pt is saved correctly
BEST_MODEL_PATH = os.path.join(OUTPUT_DIR, "best.pt")
if os.path.exists(BEST_MODEL_PATH):
    print(f"Training completed successfully! Best model saved at: {BEST_MODEL_PATH}")
else:
    print("Training failed: best.pt not found!")
    exit(1)
