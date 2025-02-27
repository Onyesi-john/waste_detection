from ultralytics import YOLO
import os
import shutil

# Load the YOLOv5n model
model = YOLO("yolov5n.pt")

# Train the model
model.train(
    data="dataset/data.yaml",  # Path to dataset configuration file
    epochs=50,
    imgsz=640,
    batch=8,
    project="waste_detection",
    name="exp",
    exist_ok=True,
)

# Locate the best.pt file
best_model_path = "waste_detection/exp/weights/best.pt"

# Check if best.pt exists
if os.path.exists(best_model_path):
    # Copy best.pt to the root directory
    shutil.copy(best_model_path, "./best.pt")
    print(f"✔ Best model saved at: {os.path.abspath('best.pt')}")
else:
    print("❌ Training failed: best.pt not found!")
